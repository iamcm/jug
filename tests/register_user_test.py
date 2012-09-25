from models import Logger
from models.EntityManager import EntityManager
from tests.BaseTest import BaseTest
from bs4 import BeautifulSoup

import mechanize



class RegisterUserTest(BaseTest):

	def setUp(self):
		self.br = mechanize.Browser()

	def register_user(self):
		resp = self.br.open(self.base_url +'/register')
		self.br.select_form(nr=0)
		self.br.form['email'] = 'an@email.com'
		self.br.form['password1'] = 'pass'
		self.br.form['password2'] = 'pass'
		self.br.submit()		
	
	def test_load_register_user_page(self):
		self.br.open(self.base_url +'/register')
		self.assertEqual(self.br.geturl(), self.base_url +'/register')

	def test_register_user(self):
		#should end up with a non valid user because they will have
		#been created but not activated

		#check we have no users at the moment
		users = [u for u in self.conn.User.find()]
		self.assertEqual(len(users),0)

		#create a user
		self.register_user()

		#get the created user
		users = [u for u in self.conn.User.find()]
		self.assertEqual(len(users),1)

		#check that they are marked as invalid
		self.assertFalse(users[0]['valid'])

	def test_activate_user(self):
		#create a user
		self.register_user()

		#get the created user
		users = [u for u in self.conn.User.find()]
		self.assertEqual(len(users),1)

		#check that they are marked as invalid
		self.assertFalse(users[0]['valid'])

		#load the activation page
		self.br.open(self.base_url +'/activate/'+ users[0]['token'])

		#get the created user now that they have been activated
		users = [u for u in self.conn.User.find()]

		#check that they are now marked as valid
		self.assertTrue(users[0]['valid'])

	def test_activation_email_is_sent(self):
		#at the moment just test that the email
		#gets logged in the site.log

		#create a user
		self.register_user()

		#get the created user
		users = [u for u in self.conn.User.find()]

		with open('./site.log', 'r') as f:
			text = f.read()

		link = '<a href="http://localhost:8080/activate/%s">Activate</a>' % users[0]['token']

		self.assertTrue(link in text)


if __name__ == '__main__':
	unittest.main()

