from models import Logger
from tests.BaseTest import BaseTest
import mechanize



class IndexTest(BaseTest):

	def setUp(self):
		self.br = mechanize.Browser()

	def test_redirect_to_login(self):
		resp = self.br.open(self.base_url)

		self.assertEquals(resp.geturl(), self.base_url +'/login')

	def test_index_page(self):
		self.create_user()
		self.login_user()

		resp = self.br.open(self.base_url)

		self.assertEquals(resp.geturl(), self.base_url)


if __name__ == '__main__':
	unittest.main()

