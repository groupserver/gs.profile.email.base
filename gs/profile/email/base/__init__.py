# coding=utf-8
from AccessControl import ModuleSecurityInfo
from AccessControl import allow_class

eu_security = ModuleSecurityInfo('gs.profile.email.base.emailuser')
eu_security.declarePublic('EmailUser')

from gs.profile.email.base.emailuser import EmailUserFromUser, EmailUser
allow_class(EmailUserFromUser)
