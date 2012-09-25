import datetime
import json
import random
import bottle

import db
from db import _DBCON
from models import Logger
from models.EntityManager import EntityManager
from models import Util
from models.Item import Item
from models.Tag import Tag
import settings
from controllers.BaseController import BaseController
from controllers.AuthController import checklogin

@checklogin
class DefaultController(BaseController):

    def index(self):
        return self._template('index')
        