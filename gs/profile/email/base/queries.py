# coding=utf-8
import sqlalchemy as sa

class UserEmailQuery(object):

    def __init__(self, user, da):
        self.context = user
        self.userId = user.getId()
        self.userEmailTable = da.createTable('user_email')
        self.emailVerificationTable = da.createTable('email_verification')

    def add_address(self, address, isPreferred=False):
        uet = self.userEmailTable
        i = uet.insert()
        i.execute(user_id=self.userId,
            email=address,
            is_preferred=isPreferred,
            verified_date=None)

    def remove_address(self, address):
        uet = self.userEmailTable        
        d = uet.delete(sa.func.lower(uet.c.email) == address.lower())
        d.execute()

    def get_addresses(self, preferredOnly=False, verifiedOnly=True):
        uet = self.userEmailTable
        s = sa.select([uet.c.email], uet.c.user_id == self.userId)
        if preferredOnly:
            s.append_whereclause(uet.c.is_preferred == preferredOnly)
        if verifiedOnly:
            s.append_whereclause(uet.c.verified_date!=None)
        r = s.execute()
        
        addresses = []
        for row in r.fetchall():
            addresses.append(row['email'])
        return addresses
    
    def get_unverified_addresses(self):
        uet = self.userEmailTable
        s = sa.select([uet.c.email], uet.c.user_id == self.userId)
        s.append_whereclause(uet.c.verified_date == None)
        r = s.execute()
        
        addresses = []
        for row in r.fetchall():
            addresses.append(row['email'])
        return addresses
    
    def is_address_verified(self, address):
        uet = self.userEmailTable
        s = uet.select(sa.func.lower(uet.c.email) == address.lower())
        r = s.execute()

        retval = False
        if r.rowcount == 1:
            retval = r.fetchone()['verified_date'] != None
        assert type(retval) == bool
        return retval
    
    def update_delivery(self, address, isPreferred):
        uet = self.userEmailTable
        u = uet.update(sa.and_(uet.c.user_id==self.userId,
                               sa.func.lower(uet.c.email) == address.lower()))
        u.execute(is_preferred=isPreferred)
        