# coding=utf-8
from pytz import UTC
from datetime import datetime
from zope.component import createObject
from zope.component.interfaces import IFactory
from zope.interface import implements, implementedBy
from Products.GSAuditTrail import IAuditEvent, BasicAuditEvent, \
  AuditQuery, event_id_from_data
from Products.XWFCore.XWFUtils import munge_date
from Products.CustomUserFolder.userinfo import userInfo_to_anchor

SUBSYSTEM = 'gs.profile.email.base'
import logging
log = logging.getLogger(SUBSYSTEM) #@UndefinedVariable

UNKNOWN         = '0'
ADD_ADDRESS     = '1'
REMOVE_ADDRESS  = '2'

class AuditEventFactory(object):
    implements(IFactory)

    title=u'Profile Email Address Audit-Event Factory'
    description=u'Creates a GroupServer audit event for profile email address actions'

    def __call__(self, context, event_id, code, date,
        userInfo, instanceUserInfo, siteInfo, groupInfo=None,
        instanceDatum='', supplementaryDatum=None, subsystem=''):
        if code == ADD_ADDRESS:
            event = AddAddressEvent(context, event_id, date, 
                        instanceUserInfo, siteInfo, instanceDatum)
        elif code == REMOVE_ADDRESS:
            event = RemoveAddressEvent(context, event_id, date, userInfo,
                        instanceUserInfo, siteInfo, instanceDatum)
        else:
            event = BasicAuditEvent(context, event_id, UNKNOWN, date, 
              userInfo, instanceUserInfo, siteInfo, groupInfo, 
              instanceDatum, supplementaryDatum, SUBSYSTEM)
        assert event
        return event
    
    def getInterfaces(self):
        return implementedBy(BasicAuditEvent)
        
class AddAddressEvent(BasicAuditEvent):
    ''' An audit-trail event representing a person adding an email address.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, siteInfo, instanceDatum):
        BasicAuditEvent.__init__(self, context, id, ADD_ADDRESS, d, 
            userInfo, userInfo, siteInfo, None, instanceDatum, 
            None, SUBSYSTEM)
    
    @property
    def adminAdded(self):
        retval = False
        if self.userInfo.id and self.userInfo.id!= self.instanceUserInfo.id:
            retval = True
        return retval
    
    def __unicode__(self):
        if self.adminAdded:
            retval = u'%s (%s) added the address '\
              '<%s> for %s (%s) on %s (%s).' %\
               (self.userInfo.name, self.userInfo.id,
                self.instanceDatum,
                self.instanceUserInfo.name, self.instanceUserInfo.id,
                self.siteInfo.name, self.siteInfo.id)
        else:
            retval = u'%s (%s) added the address '\
              '<%s> on %s (%s).' %\
               (self.instanceUserInfo.name, self.instanceUserInfo.id,
                self.instanceDatum,
                self.siteInfo.name, self.siteInfo.id)
        return retval
        
    def __str__(self):
        retval = unicode(self).encode('ascii', 'ignore')
        return retval
    
    @property
    def xhtml(self):
        cssClass = u'audit-event gs-profile-email-%s' %\
          self.code
        if self.adminAdded:
            retval = u'<span class="%s">%s added the address '\
              u'<code class="email">%s</code>.</span>' % \
              (cssClass, userInfo_to_anchor(self.userInfo), 
               self.instanceDatum)
        else:
            retval = u'<span class="%s">Added the address '\
              u'<code class="email">%s</code>.</span>' % \
              (cssClass, self.instanceDatum)
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
        return retval
    
class RemoveAddressEvent(BasicAuditEvent):
    ''' An audit-trail event representing a person removing 
        an email address.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, instanceUserInfo, 
                 siteInfo, instanceDatum):
        BasicAuditEvent.__init__(self, context, id,  REMOVE_ADDRESS, d, 
            userInfo, instanceUserInfo, siteInfo, None, instanceDatum, 
            None, SUBSYSTEM)

    def __unicode__(self):
        retval = u'%s (%s) removed the email address <%s> on %s (%s).' %\
           (self.userInfo.name, self.userInfo.id,
            self.instanceDatum,
            self.siteInfo.name, self.siteInfo.id)
        return retval
        
    def __str__(self):
        retval = unicode(self).encode('ascii', 'ignore')
        return retval
    
    @property
    def xhtml(self):
        cssClass = u'audit-event gs-profile-email-%s' %\
          self.code
        retval = u'<span class="%s">Removed the address '\
          u'<code class="email">%s</code>.</span>' % \
          (cssClass, self.instanceDatum)
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))

class Auditor(object):
    def __init__(self, context, siteInfo):
        self.siteInfo = siteInfo
        self.context = context
        da = context.zsqlalchemy
        self.queries = AuditQuery(da)
        self.factory = AuditEventFactory()
        
    def info(self, code, instanceUserInfo='', instanceDatum = '', 
                supplementaryDatum = ''):
        d = datetime.now(UTC)
        userInfo = createObject('groupserver.LoggedInUser', self.context)
        instanceUserInfo = instanceUserInfo and instanceUserInfo or userInfo 
        eventId = event_id_from_data(userInfo, instanceUserInfo, 
                    self.siteInfo, code,
                    instanceDatum, supplementaryDatum)
          
        e = self.factory(self.context, eventId,  code, d, 
                userInfo, instanceUserInfo, self.siteInfo, None,
                instanceDatum, supplementaryDatum, SUBSYSTEM)
          
        self.queries.store(e)
        log.info(e)

