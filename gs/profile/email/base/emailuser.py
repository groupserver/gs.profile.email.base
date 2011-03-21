# coding=utf-8
import rfc822
from zope.interface import implements, Interface
from zope.component import adapts, createObject
from zope.schema import ValidationError
from Products.CustomUserFolder.interfaces import ICustomUser, IGSUserInfo
from queries import UserEmailQuery
from interfaces import IGSEmailUser
from audit import Auditor, ADD_ADDRESS, REMOVE_ADDRESS
from audit import DELIVERY_ON, DELIVERY_OFF

class EmailUser(object):
    implements(IGSEmailUser)
    adapts(Interface, IGSUserInfo)
    
    def __init__(self, context, userInfo):
        self.context = context
        self.userInfo = userInfo
        self.__auditor = self.__siteInfo = None
        self.__query = None
    
    @property
    def query(self):
        if self.__query == None:
            self.__query = UserEmailQuery(self.userInfo.user, 
                            self.context.zsqlalchemy)
        return self.__query
    
    @property
    def auditor(self):
        if self.__auditor == None:
            self.__auditor = Auditor(self.context, self.siteInfo)
        return self.__auditor

    @property
    def siteInfo(self):
        if self.__siteInfo == None:
            self.__siteInfo = \
              createObject('groupserver.SiteInfo', self.context)
        return self.__siteInfo
    
    def add_address(self, address, isPreferred=False):
        assert address not in self.get_addresses(), \
          '%s (%s) already has the address <%s>' % \
           (self.userInfo.name, self.userId, address)
        address = self._validateAndNormalizeEmail(address)
        self.query.add_address(address, isPreferred)
        self.auditor.info(ADD_ADDRESS, self.userInfo, address)
        
    def remove_address(self, address):
        assert address in self.get_addresses(), \
          '%s (%s) does not have the address <%s>' % \
           (self.userInfo.name, self.userId, address)
        address = self._validateAndNormalizeEmail(address)
        self.query.remove_address(address)
        self.auditor.info(REMOVE_ADDRESS, self.userInfo, address)
        
    def is_address_verified(self, address):
        assert address in self.get_addresses(), \
          '%s (%s) does not have the address <%s>' % \
           (self.userInfo.name, self.userId, address)
        return self.query.is_address_verified(address)
    
    def get_addresses(self):
        # --=mpj17=-- Note that registration requires this to be able
        #   to return all the user's email addresses, not just the 
        #   verified addresses.
        return self.query.get_addresses(preferredOnly=False, verifiedOnly=False)

    def get_verified_addresses(self):
        return self.query.get_addresses(preferredOnly=False, verifiedOnly=True)    

    def get_unverified_addresses(self):
        return self.query.get_unverified_addresses()
        
    def get_delivery_addresses(self):
        return self.query.get_addresses(preferredOnly=True)
    
    def set_delivery(self, address):
        address = self._validateAndNormalizeEmail(address)
        allAddresses = self.get_addresses()
    
        # If we don't have the email address in the database yet, 
        #  add it and set it for preferred delivery
        if address not in allAddresses:
            self.add_address(address, isPreferred=True)
        # Otherwise, just set it for preferred delivery
        else:
            self.query.update_delivery(address, isPreferred=True)
        self.auditor.info(DELIVERY_ON, self.userInfo, address)
        
    def drop_delivery(self, address):
        address = self._validateAndNormalizeEmail(address)
        self.query.update_delivery(address, isPreferred=False)
        self.auditor.info(DELIVERY_OFF, self.userInfo, address)        

    def _validateAndNormalizeEmail(self, address):
        """ Validates and normalizes an email address.
        """
        address = address.strip()
        if not address:
            raise ValidationError('No email address given')
        try:
            a = rfc822.AddressList(address)
        except:
            raise ValidationError('Email address was not compliant with rfc822')
        if len(a.addresslist) > 1:
            raise ValidationError('More than one email address was given')
        try:
            address = a.addresslist[0][1]
        except:
            raise ValidationError('Unexpected validation error')
        if not address:
            raise ValidationError('No email address given')
        return address

class EmailUserFromEmailAddressFactory(object):
    """ Create an EmailUser from an email address.
    """
    def __call__(self, context, address):
        retval = None
        aclUsers = context.site_root().acl_users
        user = aclUsers.get_userByEmail(address)
        if user:
            userInfo = IGSUserInfo(user)
            retval = EmailUser(context, userInfo) 
        return retval
        
class EmailUserFromUser(EmailUser):
    implements( IGSEmailUser )
    adapts( ICustomUser )
    def __init__(self, user):
        userInfo = IGSUserInfo(user)
        EmailUser.__init__(self, user, userInfo)
        
