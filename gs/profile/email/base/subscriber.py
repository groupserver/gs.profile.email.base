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
from logging import getLogger
log = getLogger('gs.profile.email.base.subscriber')
from .interfaces import IGSEmailUser


def remove_email_data(user, event):
    '''A subscriber for the ``remove`` event. Deletes the email address
from the relational database when the profile for the user is deleted.'''
    log.info('Removing addresses for {0}'.format(user.getId()))
    emailUser = IGSEmailUser(user)
    for address in emailUser.get_addresses():
        emailUser.remove_address(address)
