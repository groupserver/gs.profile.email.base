# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import
from email.utils import parseaddr
from operator import or_
from re import compile as re_compile, IGNORECASE
from zope.schema import ASCIILine, ValidationError

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

# --=mpj17=-- The email regular expression (EMAIL_RE) below is more
#   strict than the standard,
#   RFC 5322 <http://tools.ietf.org/html/rfc5322#section-3.4.1>.
#   The checker sould be changed to be more flexible.
#
#   addr-spec       =   local-part "@" domain
#
#   local-part      =   dot-atom / quoted-string / obs-local-part
#
#   dot-atom        =   [CFWS] dot-atom-text [CFWS]
#
#   dot-atom-text   =   1*atext *("." 1*atext)
#
#   atom            =   [CFWS] 1*atext [CFWS]
#
#   atext           =   ALPHA / DIGIT /    ; Printable US-ASCII
#                       "!" / "#" /        ;  characters not including
#                       "$" / "%" /        ;  specials.  Used for atoms.
#                       "&" / "'" /
#                       "*" / "+" /
#                       "-" / "/" /
#                       "=" / "?" /
#                       "^" / "_" /
#                       "`" / "{" /
#                       "|" / "}" /
#                       "~"
#
EMAIL_RE = r'\b[a-z0-9\._%+-]+@([a-z0-9\-]+\.)+[a-z]{2,4}\b'
emailRE = re_compile(EMAIL_RE, IGNORECASE)


def check_email(addr):
    r = parseaddr(addr)
    return emailRE.match(r[1]) is not None


BANNED_DOMAINS = ['dodgit.com', 'enterto.com', 'myspamless.com',
  'e4ward.com', 'guerrillamail.biz', 'jetable.net', 'mailinator.com',
  'mintemail.com', 'vansoftcorp.com', 'plasticinbox.com', 'pookmail.com',
  'shieldedmail.net', 'sneakemail.com', 'spamgourmet.com', 'spambox.us',
  'spaml.com', 'temporaryinbox.com', 'mx0.wwwnew.eu', 'bodhi.lawlita.com',
  'mail.htl22.at', 'zoemail.net', 'despam.it']


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
        m = u'The text "{0}" is not a valid email address.'
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
        return u'The email address "%s" is from a disposable '\
          u'email-address provider; disposable '\
          u'email-addresses cannot be used with this site.' % self.value

    def doc(self):
        return self.__str__()


class EmailAddress(ASCIILine):
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
        return u'The email address "%s" already exists on this site.' % \
          self.value

    def doc(self):
        return self.__str__()


class NewEmailAddress(EmailAddress):
    def constraint(self, value):
        EmailAddress.constraint(self, value)
        if address_exists(self.context, value):
            raise EmailAddressExists(value)
        return True
