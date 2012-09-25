import datetime
import bottle
from Crypto.Hash import SHA
from models.BaseModel import BaseModel
import settings

class Session(BaseModel):
    
    def __init__(self, DBCON, publicid=None):
        self.fields = [
            ('publicid', None),
            ('userid', None),
            ('data', False),
            ('ip', None),
            ('useragent', None),
            ('added', datetime.datetime.now()),
            ('expires', self.get_expires()),
            ('valid', True),
        ]
        self.init(DBCON)
        
        if publicid:
            self.get_session(publicid)
            
    def get_session(self, publicid):
        session = self.db.Session.find_one({
            'publicid': publicid,
            'valid': True,
        })
        
        if session:
            setattr(self, '_id', session.get('_id'))
            for f, val in self._fields:
                setattr(self, f, session.get(f))
        else:
            self.valid = False
    
    
    def get_expires(self):
        now = datetime.datetime.utcnow()
        delta = datetime.timedelta(hours=settings.SESSIONDURATION)
        return now + delta
        
    
    def save(self):
        if not self._id:
            self._id = self.db.Session.save({})
            
            # Hash the mongo session id so we can store it in a cookie.
            # By doing this users shouldnt be able to simply increment
            # their 'token' cookie value and gain access to someone elses
            # session
            h = SHA.new()
            h.update(str(self._id))
            self.publicid = h.hexdigest()
        
        # If this is a persistant session then update the cookie expiry time
        if settings.SESSIONISPERSISTENT:
            self.set_cookie()

        super(self.__class__, self).save()
        
        
    def check(self, ip, useragent):
        if self.expires > datetime.datetime.utcnow()\
        and self.useragent==useragent:
            self.expires = self.get_expires()
            
            self.save()
            return True
        else:
            self.valid = False
            return False
        
        
    def destroy(self):
        self.valid = False
        # destroy the persistent cookie if it exists
        if settings.SESSIONISPERSISTENT:
            bottle.response.set_cookie('token', '', expires=datetime.datetime.now() - datetime.timedelta(days=1))
        self.save()
        
    def set_cookie(self):
        if settings.SESSIONISPERSISTENT:
            bottle.response.set_cookie('token', str(self.publicid),\
                                       expires=datetime.datetime.now() + datetime.timedelta(hours=settings.SESSIONDURATION),\
                                        httponly=True, path='/')
        
        else:
            bottle.response.set_cookie('token', str(self.publicid))
    
    
        