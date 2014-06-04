# -*- coding: utf-8 -*-
##############################################################################
#
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
##############################################################################
from __future__ import absolute_import, unicode_literals
from mock import MagicMock
from unittest import TestCase
from gs.profile.email.base.groupemailuser import (GroupEmailUser,
                                                    GroupEmailSetting)
import gs.profile.email.base.groupemailuser  # lint:ok


class FauxInfo(object):
    'Not a user'


class TestGroupEmailUser(TestCase):
    'Test the GroupEmailUser class'

    def setUp(self):
        self.fauxUser = FauxInfo()
        self.fauxUser.id = 'exampleUser'
        self.fauxGroup = FauxInfo()
        self.fauxGroup.id = 'exampleGroup'
        self.fauxGroup.siteInfo = FauxInfo()
        self.fauxGroup.siteInfo.id = 'exampleSite'

    def test_get_delivery_setting_webonly(self):
        MockGUEQ = gs.profile.email.base.groupemailuser.GroupUserEmailQuery
        MockGUEQ.__init__ = MagicMock(return_value=None)
        MockGUEQ.get_groupEmailSetting = MagicMock(return_value='webonly')

        groupEmailUser = GroupEmailUser(self.fauxUser, self.fauxGroup)
        r = groupEmailUser.get_delivery_setting()

        self.assertEqual(1, MockGUEQ.get_groupEmailSetting.call_count)
        self.assertEqual(GroupEmailSetting.webonly, r)

    def test_get_delivery_setting_digest(self):
        MockGUEQ = gs.profile.email.base.groupemailuser.GroupUserEmailQuery
        MockGUEQ.__init__ = MagicMock(return_value=None)
        MockGUEQ.get_groupEmailSetting = MagicMock(return_value='digest')

        groupEmailUser = GroupEmailUser(self.fauxUser, self.fauxGroup)
        r = groupEmailUser.get_delivery_setting()

        self.assertEqual(1, MockGUEQ.get_groupEmailSetting.call_count)
        self.assertEqual(GroupEmailSetting.digest, r)

    def test_get_delivery_setting_default(self):
        MockGUEQ = gs.profile.email.base.groupemailuser.GroupUserEmailQuery
        MockGUEQ.__init__ = MagicMock(return_value=None)
        MockGUEQ.get_groupEmailSetting = MagicMock(return_value='askdjhfasdkf')
        MockGUEQ.get_groupUserEmail = MagicMock(return_value=[])

        groupEmailUser = GroupEmailUser(self.fauxUser, self.fauxGroup)
        r = groupEmailUser.get_delivery_setting()

        self.assertEqual(1, MockGUEQ.get_groupEmailSetting.call_count)
        self.assertEqual(GroupEmailSetting.default, r)

    def test_get_delivery_setting_specific(self):
        MockGUEQ = gs.profile.email.base.groupemailuser.GroupUserEmailQuery
        MockGUEQ.__init__ = MagicMock(return_value=None)
        MockGUEQ.get_groupEmailSetting = MagicMock(return_value='askdjhfasdkf')
        MockGUEQ.get_groupUserEmail = MagicMock(return_value=['eg@example.com'])

        groupEmailUser = GroupEmailUser(self.fauxUser, self.fauxGroup)
        r = groupEmailUser.get_delivery_setting()

        self.assertEqual(1, MockGUEQ.get_groupEmailSetting.call_count)
        self.assertEqual(GroupEmailSetting.specific, r)
