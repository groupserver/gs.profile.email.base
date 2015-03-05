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
from __future__ import unicode_literals
import sys
if (sys.version_info < (3, )):
    stringtype = basestring
else:
    stringtype = str
from email.utils import parseaddr


def sanitise_address(emailAddress):
    if not isinstance(emailAddress, stringtype):
        m = '{0} is not a string'.format(type(emailAddress))
        raise TypeError(m)

    addrName, retval = parseaddr(emailAddress)
    retval = retval.strip(',.!?; \t\n\r<>(){}[]')

    assert isinstance(retval, stringtype)
    return retval
