# coding=utf-8
from zope.component import createObject
from zope.interface import implements, providedBy
from zope.interface.common.mapping import IEnumerableMapping
from zope.schema.interfaces import IVocabulary, \
  IVocabularyTokenized, ITitledTokenizedTerm
from zope.schema.vocabulary import SimpleTerm 

class EmailAddressesForUser(object):
    implements(IVocabulary, IVocabularyTokenized)
    __used_for__ = IEnumerableMapping

    def __init__(self, userInfo):
        self.emailUser = EmailUser(userInfo)
        self.__addresses = None

    @property
    def addresses(self):
        if self.__addresses == None:
            self.__addresses = \
              self.emailUser.get_verified_addresses()
        assert type(self.__addresses) == list
        return self.__addresses
        
    def __iter__(self):
        """See zope.schema.interfaces.IIterableVocabulary"""
        retval = [SimpleTerm(a, a, a) 
                  for a in self.addresses]
        for term in retval:
            assert term
            assert ITitledTokenizedTerm in providedBy(term)
            #assert term.token == term.value
        return iter(retval)

    def __len__(self):
        """See zope.schema.interfaces.IIterableVocabulary"""
        return len(self.addresses)

    def __contains__(self, value):
        """See zope.schema.interfaces.IBaseVocabulary"""
        retval = value in self.addresses
        assert type(retval) == bool
        return retval

    def getQuery(self):
        """See zope.schema.interfaces.IBaseVocabulary"""
        return None

    def getTerm(self, value):
        """See zope.schema.interfaces.IBaseVocabulary"""
        return self.getTermByToken(value)
        
    def getTermByToken(self, token):
        """See zope.schema.interfaces.IVocabularyTokenized"""
        for a in self.addresses:
            if a == token:
                retval = SimpleTerm(a, a, a) 
                assert retval
                assert ITitledTokenizedTerm in providedBy(retval)
                #assert retval.token == retval.value
                return retval
        raise LookupError, token

class EmailAddressesForLoggedInUser(EmailAddressesForUser):
    """ Similar to EmailAddressesForUser, but makes the assumption
        that we always want the addresses of the user that is logged in.
    """
    def __init__(self, context):
        userInfo = createObject('groupserver.LoggedInUser', context)
        self.emailUser = EmailUser(userInfo)
        self.__addresses = None
