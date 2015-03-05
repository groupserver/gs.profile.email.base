# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2015 OnlineGroups.net and Contributors.
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
from unittest import TestCase
from gs.profile.email.base.emailaddress import check_email


class TestCheckAddress(TestCase):
    'Checking the check_email function'

    def test_simple(self):
        'A simple email address'
        r = check_email('member@example.com')
        self.assertTrue(r)

    def test_friendly(self):
        'Test an email address with a "friendly" part'
        r = check_email('A. Member <member@example.com>')
        self.assertTrue(r)

    def test_gmail_friendly(self):
        'Test an email address with a "friendly" part and a GMail style +'
        r = check_email('A. Member <member+list@example.com>')
        self.assertTrue(r)

    def test_no_at(self):
        'Test an email address that is devoid of an @'
        r = check_email('Tonight on Ethyl the Frog we look at violence')
        self.assertFalse(r)
