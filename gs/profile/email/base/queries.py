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
import sqlalchemy as sa
from zope.sqlalchemy import mark_changed
from gs.database import getTable, getSession


class UserEmailQuery(object):

    def __init__(self, user, da=None):
        self.userId = user.getId()
        self.userEmailTable = getTable('user_email')
        self.emailVerificationTable = getTable('email_verification')

    def add_address(self, address, isPreferred=False):
        uet = self.userEmailTable
        i = uet.insert()
        d = {'user_id': self.userId,
             'email': address,
             'is_preferred': isPreferred,
             'verified_date': None}

        session = getSession()
        session.execute(i, params=d)
        mark_changed(session)

    def remove_address(self, address):
        uet = self.userEmailTable
        d = uet.delete(sa.func.lower(uet.c.email) == address.lower())

        session = getSession()
        session.execute(d)
        mark_changed(session)

    def get_addresses(self, preferredOnly=False, verifiedOnly=True):
        uet = self.userEmailTable
        s = sa.select([uet.c.email])
        s.append_whereclause(uet.c.user_id == self.userId)
        if preferredOnly:
            s.append_whereclause(uet.c.is_preferred == preferredOnly)
        if verifiedOnly:
            s.append_whereclause(uet.c.verified_date != None)  # lint:ok
        session = getSession()
        r = session.execute(s)
        addresses = []
        for row in r.fetchall():
            addresses.append(row['email'])
        return addresses

    def get_unverified_addresses(self):
        uet = self.userEmailTable
        s = sa.select([uet.c.email], uet.c.user_id == self.userId)
        s.append_whereclause(uet.c.verified_date == None)  # lint:ok

        session = getSession()
        r = session.execute(s)
        addresses = []
        for row in r.fetchall():
            addresses.append(row['email'])
        return addresses

    def is_address_verified(self, address):
        uet = self.userEmailTable
        s = sa.select([uet.c.verified_date], limit=1)
        s.append_whereclause(sa.func.lower(uet.c.email) == address.lower())

        session = getSession()
        r = session.execute(s)
        retval = False
        if r.rowcount == 1:
            retval = r.fetchone()['verified_date'] is not None
        assert type(retval) == bool
        return retval

    def update_delivery(self, address, isPreferred):
        uet = self.userEmailTable
        u = uet.update(sa.and_(uet.c.user_id == self.userId,
                               sa.func.lower(uet.c.email) == address.lower()))
        d = {'is_preferred': isPreferred, }

        session = getSession()
        session.execute(u, params=d)
        mark_changed(session)
