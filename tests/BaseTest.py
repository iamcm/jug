import unittest
from models.User import User
from pymongo import Connection
import settings
import mechanize
from models import Logger

class BaseTest(unittest.TestCase):
	"""
	Provides test classes with common functionality
	"""
	def __init__(self, methodName='runTest'):
		Connection().drop_database('test')
		self.conn = Connection(settings.DBHOST, settings.DBPORT).test
		self.base_url = 'http://localhost:8080'
		unittest.TestCase.__init__(self, methodName=methodName)

	def drop_test_database(self):
		Connection().drop_database('test')

	def create_user(self, email='a@a.com', password='passpass', valid=True):
		u = User(self.conn)
		u.email = email
		u.password = password
		u.valid = valid
		u.save()

		return u

	def login_user(self, email='a@a.com', password='passpass'):
		resp = self.br.open(self.base_url)
		self.br.select_form(nr=0)
		self.br.form['email'] = email
		self.br.form['password'] = password
		self.br.submit()

	def tearDown(self):
		self.drop_test_database()



