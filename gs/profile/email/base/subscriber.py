# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from logging import getLogger
log = getLogger('gs.profile.email.base.subscriber')
from .interfaces import IGSEmailUser


def remove_email_data(user, event):
    log.info('Removing addresses for {0}'.format(user.getId()))
    emailUser = IGSEmailUser(user)
    for address in emailUser.get_addresses():
        emailUser.remove_address(address)
