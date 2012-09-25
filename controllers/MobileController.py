import json

import bottle

import settings
from db import _DBCON
from controllers.BaseController import BaseController
from controllers.AuthController import checklogin
from models.EntityManager import EntityManager
from models.Tag import Tag
from models.Item import Item

#@checklogin
class MobileController(BaseController):

    def index(self):
        return json.dumps({
            'hello':'world'
        })

