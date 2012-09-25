import bottle
from bottle import route
from controllers.DefaultController import DefaultController
from controllers.AuthController import AuthController
from controllers.MobileController import MobileController
import settings

########## STATIC FILES ##############
if settings.PROVIDE_STATIC_FILES:
    @route('/static/<filepath:path>')
    def index(filepath):
        return bottle.static_file(filepath, root=settings.ROOTPATH +'/static/')
        
    @route('/userfiles/<filepath:path>')
    def index(filepath):
        return bottle.static_file(filepath, root=settings.ROOTPATH +'/userfiles/') 
######################################

########## AUTH ##############
@route('/login', method='GET')
def index():
    return AuthController().index()

@route('/login', method='POST')
def index():
    e = bottle.request.POST.get('email')
    p = bottle.request.POST.get('password')
    return AuthController().login(e, p)

@route('/logout', method='GET')
def index():
    return AuthController().logout()

"""
@route('/register', method='GET')
def index():
    return AuthController().register()

@route('/register', method='POST')
def index():
    return AuthController().register_post()

@route('/success', method='GET')
def index():
    return AuthController().register_success()

@route('/activate/<token>')
def index(token):
    return AuthController().activate_token(token)
"""
##############################



##############################
###### MAIN APP ROUTES #######
##############################
@route('/', method='GET') 
def index():
    return DefaultController().index()

##############################
######### MOBILE #############
##############################
@route('/mobile/login', method='POST') 
def index():
    e = bottle.request.POST.get('email')
    p = bottle.request.POST.get('password')

    return AuthController().login_mobile(e, p)


@route('/mobile/', method='GET') 
def index():
    return MobileController().index()
