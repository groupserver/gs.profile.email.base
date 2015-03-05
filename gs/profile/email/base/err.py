# -*- coding: utf-8 -*-
############################################################################
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
############################################################################
from __future__ import absolute_import, unicode_literals


class AddressError(ValueError):

    def __init__(self, msg, address, userId):
        super(AddressError, self).__init__(msg)
        self.address = address
        self.userId = userId


class AddressMissingError(AddressError):
    'The user does lacks an address that he or she should have.'
    def __init__(self, msg, address, userId):
        super(AddressMissingError, self).__init__(msg, address, userId)


class AddressExistsError(AddressError):
    'The user has an address that he or she should lack.'
    def __init__(self, msg, address, userId):
        super(AddressExistsError, self).__init__(msg, address, userId)
