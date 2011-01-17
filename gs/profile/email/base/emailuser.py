# coding=utf-8
from zope.interface import implements
from zope.component import adapts
from Products.CustomUserFolder.interfaces import IGSUserInfo
from queries import UserEmailQuery
from interfaces import IGSEmailUser
from audit import Auditor

class EmailUser(object):
    implements(IGSEmailUser)
    adapts(IGSUserInfo)
    
    def __init__(self, userInfo):
        self.userInfo = userInfo
        self.__auditor = self.__siteInfo = None
    
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
        """ Add the given email address to the user's profile.
        """
        assert address not in self.get_addresses(), \
          '%s (%s) already has the address <%s>' % \
           (self.userInfo.name, self.userId, address)
        address = self._validateAndNormalizeEmail(address)
        uq = UserEmailQuery(self.userInfo.user, self.zsqlalchemy)        
        uq.add_address(address, isPreferred)
        self.auditor.info(ADD_ADDRESS, self.userInfo, address)
        
    def remove_address(self, address):
        """ Remove the given email address from the profile.
        """
        assert address in self.get_addresses(), \
          '%s (%s) does not have the address <%s>' % \
           (self.userInfo.name, self.userId, address)
        address = self._validateAndNormalizeEmail(address)
        uq = UserEmailQuery(self.userInfo.user, self.zsqlalchemy)
        uq.remove_address(address)
        self.auditor.info(REMOVE_ADDRESS, self.userInfo, address)
        
    def is_address_verified(self, address):
        """ Check to see if the given address is verified.
        """
        assert address in self.get_addresses(), \
          '%s (%s) does not have the address <%s>' % \
           (self.userInfo.name, self.userId, address)
        uq = UserEmailQuery(self.userInfo.user, self.zsqlalchemy)
        return uq.is_address_verified(address)
    
    def get_addresses(self):
        """ Returns a list of all the user's email addresses.
            A helper method to purify the list of addresses.
        """
        # --=mpj17=-- Note that registration requires this to be able
        #   to return all the user's email addresses, not just the 
        #   verified addresses.
        uq = UserQuery(self, self.zsqlalchemy)
        return uq.get_addresses(preferredOnly=False, verifiedOnly=False)

    def get_verified_addresses(self):
        """Get all the user's verified email addresses.
        """
        uq = UserEmailQuery(self.userInfo.user, self.zsqlalchemy)
        return uq.get_addresses(preferredOnly=False, verifiedOnly=True)    
        
    def get_delivery_addresses(self):
        """ Get all the user's default delivery addresses.
        """
        uq = UserEmailQuery(self.userInfo.user, self.zsqlalchemy)
        return uq.get_addresses(preferredOnly=True)
    
    def set_delivery(self, address):
        """ Set the given email address to be a default
            delivery address.
        """
        
    def drop_delivery(self, address):
        """ Set the given address to no longer be a default
            delivery address.
        """

    security.declarePrivate('_validateAndNormalizeEmail')
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
