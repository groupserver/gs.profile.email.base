# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014, 2015 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals
from email.utils import parseaddr
from operator import or_
from re import compile as re_compile, IGNORECASE
from zope.schema import TextLine, ValidationError

__context_acl_users = {}


def __get_acl_users_for_context(context):
    assert context
    if context not in __context_acl_users:
        acl_users = context.site_root().acl_users
        __context_acl_users[context] = acl_users
    else:
        acl_users = __context_acl_users[context]
    assert acl_users
    return acl_users
get_acl_users_for_context = __get_acl_users_for_context

# --=mpj17=-- The email regular expression (EMAIL_RE) below fails to conform
#   to the standard,
#   RFC 5322 <http://tools.ietf.org/html/rfc5322#section-3.4.1>.
# It is taken from the HTML5 spec
# <https://html.spec.whatwg.org/multipage/forms.html#e-mail-state-%28type=email%29>
EMAIL_RE = r"\b[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9]"\
           r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9]"\
           r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\b"
emailRE = re_compile(EMAIL_RE, IGNORECASE)


def check_email(addr):
    r = parseaddr(addr)
    return emailRE.match(r[1]) is not None


BANNED_DOMAINS = [
    'dodgit.com', 'enterto.com', 'myspamless.com',
    'e4ward.com', 'guerrillamail.biz', 'jetable.net', 'mailinator.com',
    'mintemail.com', 'vansoftcorp.com', 'plasticinbox.com', 'pookmail.com',
    'shieldedmail.net', 'sneakemail.com', 'spamgourmet.com', 'spambox.us',
    'spaml.com', 'temporaryinbox.com', 'mx0.wwwnew.eu', 'bodhi.lawlita.com',
    'mail.htl22.at', 'zoemail.net', 'despam.it', ]


def address_exists(context, addr):
    n, e = parseaddr(addr)
    acl_users = get_acl_users_for_context(context)
    user = acl_users.get_userIdByEmail(e)
    retval = user is not None
    assert type(retval) == bool
    return retval


def disposable_address(addr):
    n, e = parseaddr(addr)
    userAddress = e.lower()
    retval = reduce(or_, [d in userAddress for d in BANNED_DOMAINS], False)
    assert type(retval) == bool
    return retval


class NotAValidEmailAddress(ValidationError):
    """Not a valid email address"""
    def __init__(self, value):
        self.value = value

    def __unicode__(self):
        m = 'The text "{0}" is not a valid email address.'
        retval = m.format(self.value)
        return retval

    def __str__(self):
        retval = unicode(self).encode('ascii', 'ignore')
        return retval

    def doc(self):
        return self.__str__()


class DisposableEmailAddressNotAllowed(ValidationError):
    """Disposable Email Addresses are Not Allowed"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'The email address "%s" is from a disposable '\
            'email-address provider; disposable '\
            'email-addresses cannot be used with this site.' % self.value

    def doc(self):
        return self.__str__()


class EmailAddress(TextLine):
    '''An email-address entry.
    '''
    def constraint(self, value):
        if not(check_email(value)):
            raise NotAValidEmailAddress(value)
        elif disposable_address(value):
            raise DisposableEmailAddressNotAllowed(value)
        # TODO: Think about banning particular addresses. GMail would
        #   scuttle any efforts to do this properly\ldots
        # AM: We've since gone in the email_blacklist direction.
        return True


class EmailAddressExists(ValidationError):
    """Email Address already exists on the system"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'The email address "%s" already exists on this site.' % \
            self.value

    def doc(self):
        return self.__str__()


class NewEmailAddress(EmailAddress):
    def constraint(self, value):
        EmailAddress.constraint(self, value)
        if address_exists(self.context, value):
            raise EmailAddressExists(value)
        return True
