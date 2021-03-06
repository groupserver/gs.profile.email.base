# -*- coding: utf-8 -*-
############################################################################
# Copyright © 2013, 2014 OnlineGroups.net and Contributors.
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
import rfc822
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from zope.schema import ValidationError
from Products.CustomUserFolder.interfaces import IGSUserInfo
from .audit import Auditor, ADD_ADDRESS, REMOVE_ADDRESS, DELIVERY_ON, \
    DELIVERY_OFF
from .err import AddressMissingError, AddressExistsError
from .queries import UserEmailQuery


class EmailUser(object):
    def __init__(self, context, userInfo):
        self.context = context
        self.userInfo = userInfo

    @Lazy
    def query(self):
        retval = UserEmailQuery(self.userInfo.user)
        return retval

    @Lazy
    def auditor(self):
        retval = Auditor(self.context, self.siteInfo)
        return retval

    @Lazy
    def siteInfo(self):
        retval = createObject('groupserver.SiteInfo', self.context)
        return retval

    def has_address(self, address):
        '''Test if the user has an email address

:param str address: The address to check. **Case insensitive.**
:returns: ``True`` the user has the ``address``.
:rtype: bool

Because email addresses are case insensitive (and you *will* get a mixture
of addresses)
'''
        l_address = address.lower()
        l_addresses = [a.lower() for a in self.get_addresses()]
        retval = l_address in l_addresses
        return retval

    def __contains__(self, a):
        'Allows ``addr in emailUser`` and ``addr not in emailUser``.'
        retval = self.has_address(a)
        return retval

    def add_address(self, address, isPreferred=False):
        if address in self:
            m = 'Cannot addd the address, as {0} ({1}) already has the ' \
                'address <{2}>.'
            msg = m.format(self.userInfo.name, self.userInfo.id, address)
            raise AddressExistsError(msg, address, self.userInfo.id)

        address = self._validateAndNormalizeEmail(address)
        self.query.add_address(address, isPreferred)
        self.auditor.info(ADD_ADDRESS, self.userInfo, address)

    def remove_address(self, address):
        if address not in self:
            m = 'Cannot remove the address, as {0} ({1}) lacks the '\
                'address <{2}>.'
            msg = m.format(self.userInfo.name, self.userInfo.id, address)
            raise AddressMissingError(msg, address, self.userInfo.id)

        address = self._validateAndNormalizeEmail(address)
        self.query.remove_address(address)
        self.auditor.info(REMOVE_ADDRESS, self.userInfo, address)

    def is_address_verified(self, address):
        if address not in self:
            m = 'Cannot verify the address, as {0} ({1}) lacks the '\
                'address <{2}>.'
            msg = m.format(self.userInfo.name, self.userInfo.id, address)
            raise AddressMissingError(msg, address, self.userInfo.id)

        retval = self.query.is_address_verified(address)
        return retval

    def get_addresses(self):
        # --=mpj17=-- Note that registration requires this to be able
        #   to return all the user's email addresses, not just the
        #   verified addresses.
        return self.query.get_addresses(preferredOnly=False,
                                        verifiedOnly=False)

    def get_verified_addresses(self):
        return self.query.get_addresses(preferredOnly=False,
                                        verifiedOnly=True)

    @property
    def verified(self):
        # --=mpj17=-- Deliberately not @Lazy, because they may change
        retval = [a.lower() for a in self.get_verified_addresses()]
        return retval

    def get_unverified_addresses(self):
        return self.query.get_unverified_addresses()

    @property
    def unverified(self):
        # --=mpj17=-- Deliberately not @Lazy, because they may change
        retval = [a.lower() for a in self.get_unverified_addresses()]
        return retval

    def get_delivery_addresses(self):
        return self.query.get_addresses(preferredOnly=True)

    @property
    def preferred(self):
        # --=mpj17=-- Deliberately not @Lazy, because they may change
        retval = [a.lower() for a in self.get_delivery_addresses()]
        return retval

    @property
    def extra(self):
        # --=mpj17=-- Deliberately not @Lazy, because they may change
        retval = list(set(self.verified) - set(self.preferred))
        return retval

    def set_delivery(self, address):
        address = self._validateAndNormalizeEmail(address)
        allAddresses = self.get_addresses()

        # If we don't have the email address in the database yet,
        #  add it and set it for preferred delivery
        if address not in allAddresses:
            self.add_address(address, isPreferred=True)
        # Otherwise, just set it for preferred delivery
        else:
            self.query.update_delivery(address, isPreferred=True)
        self.auditor.info(DELIVERY_ON, self.userInfo, address)

    def drop_delivery(self, address):
        address = self._validateAndNormalizeEmail(address)
        self.query.update_delivery(address, isPreferred=False)
        self.auditor.info(DELIVERY_OFF, self.userInfo, address)

    def _validateAndNormalizeEmail(self, address):
        """ Validates and normalizes an email address."""
        address = address.strip()
        if not address:
            raise ValidationError('No email address given')
        try:
            a = rfc822.AddressList(address)
        except:
            raise ValidationError('Email address was not compliant with '
                                  'rfc822')
        if len(a.addresslist) > 1:
            raise ValidationError('More than one email address was given')
        try:
            address = a.addresslist[0][1]
        except:
            raise ValidationError('Unexpected validation error')
        if not address:
            raise ValidationError('No email address given')
        return address


class EmailUserFromEmailAddressFactory(object):
    """ Create an EmailUser from an email address."""
    def __call__(self, context, address):
        retval = None
        aclUsers = context.site_root().acl_users
        user = aclUsers.get_userByEmail(address)
        if user:
            userInfo = IGSUserInfo(user)
            retval = EmailUser(context, userInfo)
        return retval


class EmailUserFromUser(EmailUser):
    def __init__(self, user):
        userInfo = IGSUserInfo(user)
        EmailUser.__init__(self, user, userInfo)
