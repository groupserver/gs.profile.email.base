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
from __future__ import absolute_import, unicode_literals
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from zope.interface import implements, providedBy
from zope.interface.common.mapping import IEnumerableMapping
from zope.schema.interfaces import IVocabulary, IVocabularyTokenized, \
    ITitledTokenizedTerm
from zope.schema.vocabulary import SimpleTerm
from Products.CustomUserFolder.interfaces import IGSUserInfo
from .emailuser import EmailUser


class EmailAddressesForUserInfo(object):
    implements(IVocabulary, IVocabularyTokenized)
    __used_for__ = IEnumerableMapping

    def __init__(self, userInfo):
        self.context = userInfo.user
        self.emailUser = EmailUser(userInfo.user, userInfo)
        self._addresses = None

    @Lazy
    def addresses(self):
        retval = self.emailUser.get_verified_addresses()
        assert type(retval) == list
        return retval

    def __iter__(self):
        """See zope.schema.interfaces.IIterableVocabulary"""
        retval = [SimpleTerm(a, a, a)
                  for a in self.addresses]
        for term in retval:
            assert term
            assert ITitledTokenizedTerm in providedBy(term)
            #assert term.token == term.value
        return iter(retval)

    def __len__(self):
        """See zope.schema.interfaces.IIterableVocabulary"""
        return len(self.addresses)

    def __contains__(self, value):
        """See zope.schema.interfaces.IBaseVocabulary"""
        retval = value in self.addresses
        assert type(retval) == bool
        return retval

    def getQuery(self):
        """See zope.schema.interfaces.IBaseVocabulary"""
        return None

    def getTerm(self, value):
        """See zope.schema.interfaces.IBaseVocabulary"""
        return self.getTermByToken(value)

    def getTermByToken(self, token):
        """See zope.schema.interfaces.IVocabularyTokenized"""
        for a in self.addresses:
            if a == token:
                retval = SimpleTerm(a, a, a)
                assert retval
                assert ITitledTokenizedTerm in providedBy(retval)
                #assert retval.token == retval.value
                return retval
        m = 'Token "{0}" not found'.format(token)
        raise LookupError(m)


class EmailAddressesForLoggedInUser(EmailAddressesForUserInfo):
    """ Similar to EmailAddressesForUser, but makes the assumption
        that we always want the addresses of the user that is logged in.
    """
    def __init__(self, context):
        self.context = context
        userInfo = createObject('groupserver.LoggedInUser', context)
        self.emailUser = EmailUser(context, userInfo)
        self._addresses = None


class EmailAddressesForUser(EmailAddressesForUserInfo):
    def __init__(self, user):
        userInfo = IGSUserInfo(user)
        self.context = user
        self.emailUser = EmailUser(userInfo.user, userInfo)
        self._addresses = None
