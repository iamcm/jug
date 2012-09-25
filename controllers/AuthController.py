import bottle

import settings
from db import _DBCON
from controllers.BaseController import BaseController
from models.User import User
from models.Session import Session
from models.Email import Email


def checklogin(callback):
    def wrapper(*args, **kwargs):
        if bottle.request.get_cookie('token') or bottle.request.GET.get('token'):
            token = bottle.request.get_cookie('token') or bottle.request.GET.get('token')
            
            s = Session(_DBCON, publicid=token)
            if not s.valid or not s.check(bottle.request.get('REMOTE_ADDR'), bottle.request.get('HTTP_USER_AGENT')):
                return bottle.redirect('/login')
            else:
                bottle.request.session = s
                return callback(*args, **kwargs)
        else:
            return bottle.redirect('/login')
    return wrapper


class AuthController(BaseController):

    def _login_user(self, u):
        s = Session(_DBCON)
        s.userid = u._id
        s.ip = bottle.request.get('REMOTE_ADDR')
        s.useragent = bottle.request.get('HTTP_USER_AGENT')
        s.save()

        return s


    def index(self):
        return self._template('login')
    
    
    def login_mobile(self, e, p):
            
        if e and p:
            u = User(_DBCON, email=e, password=p)
            
            if u._id:
                s = self._login_user(u)
                return s.publicid

        return bottle.HTTPError(403, 'Access denied')

    
    
    def login(self, e, p):
            
        if e and p:
            u = User(_DBCON, email=e, password=p)
            
            if u._id:
                s = self._login_user(u)

                s.set_cookie()

                bottle.redirect('/')

            else:
                self.viewdata.update({
                    'error':'Incorrect email/password combination', 
                    'email':e, 
                    'password':p
                })

                return self._template('login')
        else:
            self.viewdata.update({
                'error':'Please complete the form', 
                'email':'', 
                'password':''
            })
            
            return self._template('login')


    @checklogin
    def logout(self):
        s = bottle.request.session
        s.destroy()
        
        return bottle.redirect('/login')
    
    
    def register(self):
        return self._template('register')
    

    def register_post(self):
        e = bottle.request.POST.get('email')
        p1 = bottle.request.POST.get('password1')
        p2 = bottle.request.POST.get('password2')
            
        if e and p1 and p2:
            if p1 != p2:
                self.viewdata.update({
                    'error':'The passwords do not match', 
                    'email':e, 
                    'password1':p1,
                    'password2':p2,
                })
                return self._template('register')
            else:
                u = User(_DBCON, email=e, password=p1)
                if u._id:
                    self.viewdata.update({
                        'error':'An account already exists for that email address', 
                        'email':e, 
                        'password1':p1,
                        'password2':p2,
                    })

                    return self._template('register')
                else:
                    u.save()
                    e = Email(recipient=e)
                    e.send('Places accounts activation', '<a href="%s/activate/%s">Activate</a>' % (settings.BASEURL, u.token))

                    return bottle.redirect('/success')
                    
                    
        else:
            self.viewdata.update({
                'error':'Please complete the form', 
                'email':e, 
                'password1':p1,
                'password2':p2,
                })

            return self._template('register')
        

    def register_success(self):
        return self._template('register-success')


    def activate_token(self, token):
        u = User(_DBCON)
        if u.activate(token):
            self._login_user(u)

        else:
            self.viewdata.update({
                'error':'The token does not match any account that is pending activation'
            })

            return self._template('error')
    
    
    