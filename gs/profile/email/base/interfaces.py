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
from zope.interface import Interface


class IGSEmailUser(Interface):
    """ A userInfo that is capable of adding and removing
        email addresses to and from their profile, and of
        setting them to and from 'default' for delivery.
    """

    def add_address(address, isPreferred):
        """ Add the given email address to the profile.
        """

    def remove_address(address):
        """ Remove the given email address from the profile.
        """

    def is_address_verified(address):
        """ Check to see if the given address is verified.
        """

    def get_addresses():
        """ Returns a list of all the user's email addresses.
            A helper method to purify the list of addresses.
        """

    def get_verified_addresses():
        """Get all the user's verified email addresses.
        """

    def get_unverified_addresses():
        """Get all the user's unverified email addresses.
        """

    def get_delivery_addresses():
        """ Get all the user's default delivery addresses.
        """

    def set_delivery(address):
        """ Set the given email address to be a default
            delivery address.
        """

    def drop_delivery(address):
        """ Set the given address to no longer be a default
            delivery address.
        """
