# -*- coding: utf-8 -*-
from __future__ import absolute_import
from AccessControl import ModuleSecurityInfo
from AccessControl import allow_class

eu_security = ModuleSecurityInfo('gs.profile.email.base.emailuser')
eu_security.declarePublic('EmailUser')

#lint:disable
from .emailuser import EmailUserFromUser, EmailUser
from .emailaddress import NewEmailAddress, EmailAddressExists
#lint:enable
allow_class(EmailUserFromUser)
