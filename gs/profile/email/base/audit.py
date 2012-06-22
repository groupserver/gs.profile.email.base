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
DELIVERY_ON     = '3'
DELIVERY_OFF    = '4'

class AuditEventFactory(object):
    implements(IFactory)

    title=u'Profile Email Address Audit-Event Factory'
    description=u'Creates a GroupServer audit event for profile email address actions'

    def __call__(self, context, event_id, code, date,
        userInfo, instanceUserInfo, siteInfo, groupInfo=None,
        instanceDatum='', supplementaryDatum=None, subsystem=''):
        if code == ADD_ADDRESS:
            event = AddAddressEvent(context, event_id, date, userInfo,
                        instanceUserInfo, siteInfo, instanceDatum)
        elif code == REMOVE_ADDRESS:
            event = RemoveAddressEvent(context, event_id, date, userInfo,
                        instanceUserInfo, siteInfo, instanceDatum)
        elif code == DELIVERY_ON:
            event = DeliveryOnEvent(context, event_id, date, userInfo,
                        instanceUserInfo, siteInfo, instanceDatum)
        elif code == DELIVERY_OFF:
            event = DeliveryOffEvent(context, event_id, date, userInfo,
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
    ''' An audit-trail event representing a person adding an email address.
    '''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, instanceUserInfo, 
                 siteInfo, instanceDatum):
        BasicAuditEvent.__init__(self, context, id, ADD_ADDRESS, d, 
            userInfo, instanceUserInfo, siteInfo, None, instanceDatum, 
            None, SUBSYSTEM)
    
    @property
    def adminAdded(self):
        retval = False
        if self.userInfo.id and (self.userInfo.id != self.instanceUserInfo.id):
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
        an email address.
    '''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, instanceUserInfo, 
                 siteInfo, instanceDatum):
        BasicAuditEvent.__init__(self, context, id,  REMOVE_ADDRESS, d, 
            userInfo, instanceUserInfo, siteInfo, None, instanceDatum, 
            None, SUBSYSTEM)

    @property
    def adminRemoved(self):
        retval = False
        if self.userInfo.id and (self.userInfo.id != self.instanceUserInfo.id):
            retval = True
        return retval

    def __unicode__(self):
        if self.adminRemoved:
            retval = u'%s (%s) removed the email address <%s> '\
              u'from %s (%s) on %s (%s).' %\
               (self.userInfo.name, self.userInfo.id,
                self.instanceDatum,
                self.instanceUserInfo.name, self.instanceUserInfo.id,
                self.siteInfo.name, self.siteInfo.id)
        else:
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
        if self.adminRemoved:
            retval = u'<span class="%s">%s removed the address '\
              u'<code class="email">%s</code>.</span>' % \
              (cssClass, userInfo_to_anchor(self.userInfo), 
               self.instanceDatum)
        else:
            retval = u'<span class="%s">Removed the address '\
              u'<code class="email">%s</code>.</span>' % \
              (cssClass, self.instanceDatum)
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))

class DeliveryOnEvent(BasicAuditEvent):
    ''' An audit-trail event representing a person setting an 
        email address to be a default address for mail delivery.
    '''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, instanceUserInfo,
                 siteInfo, instanceDatum):
        BasicAuditEvent.__init__(self, context, id, DELIVERY_ON, d, 
            userInfo, instanceUserInfo, siteInfo, None, instanceDatum, 
            None, SUBSYSTEM)
    
    @property
    def adminSet(self):
        retval = False
        if self.userInfo.id and (self.userInfo.id != self.instanceUserInfo.id):
            retval = True
        return retval
    
    def __unicode__(self):
        if self.adminSet:
            retval = u'%s (%s) set the address <%s> for '\
              '%s (%s) for default delivery on %s (%s).' %\
               (self.userInfo.name, self.userInfo.id,
                self.instanceDatum,
                self.instanceUserInfo.name, self.instanceUserInfo.id,
                self.siteInfo.name, self.siteInfo.id)
        else:
            retval = u'%s (%s) set the address '\
              '<%s> for default delivery on %s (%s).' %\
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
        if self.adminSet:
            retval = u'<span class="%s">%s set the address '\
              u'<code class="email">%s</code> for default '\
              u'delivery.</span>' % \
              (cssClass, userInfo_to_anchor(self.userInfo), 
               self.instanceDatum)
        else:
            retval = u'<span class="%s">Set the address '\
              u'<code class="email">%s</code> for default '\
              u'delivery.</span>' % \
              (cssClass, self.instanceDatum)
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
        return retval

class DeliveryOffEvent(BasicAuditEvent):
    ''' An audit-trail event representing a person setting an 
        email address to no longer be a default address for 
        mail delivery.
    '''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, instanceUserInfo,
                 siteInfo, instanceDatum):
        BasicAuditEvent.__init__(self, context, id, DELIVERY_OFF, d, 
            userInfo, instanceUserInfo, siteInfo, None, instanceDatum, 
            None, SUBSYSTEM)
    
    @property
    def adminSet(self):
        retval = False
        if self.userInfo.id and (self.userInfo.id != self.instanceUserInfo.id):
            retval = True
        return retval
    
    def __unicode__(self):
        if self.adminSet:
            retval = u'%s (%s) removed the address <%s> for '\
              '%s (%s) from default delivery on %s (%s).' %\
               (self.userInfo.name, self.userInfo.id,
                self.instanceDatum,
                self.instanceUserInfo.name, self.instanceUserInfo.id,
                self.siteInfo.name, self.siteInfo.id)
        else:
            retval = u'%s (%s) removed the address '\
              '<%s> from default delivery on %s (%s).' %\
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
        if self.adminSet:
            retval = u'<span class="%s">%s removed the address '\
              u'<code class="email">%s</code> from default '\
              u'delivery.</span>' % \
              (cssClass, userInfo_to_anchor(self.userInfo), 
               self.instanceDatum)
        else:
            retval = u'<span class="%s">Removed the address '\
              u'<code class="email">%s</code> from default '\
              u'delivery.</span>' % \
              (cssClass, self.instanceDatum)
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
        return retval

class Auditor(object):
    def __init__(self, context, siteInfo):
        self.siteInfo = siteInfo
        self.context = context
        self.queries = AuditQuery()
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

