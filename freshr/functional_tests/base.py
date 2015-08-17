from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import sys
import time

class FunctionalTest(StaticLiveServerTestCase):

	@classmethod
	def setUpClass(cls):
		for arg in sys.argv:
			if 'liveserver' in arg:
				cls.server_url = 'http://' + arg.split('=')[1]
				return
		super().setUpClass()
		cls.server_url = cls.live_server_url

	@classmethod
	def tearDownClass(cls):
		if cls.server_url == cls.live_server_url:
			super().tearDownClass()

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def go_to_sell_page(self):
		sell_button = self.browser.find_element_by_id('sell_fish')
		sell_button.send_keys(Keys.ENTER)
		time.sleep(1)
		self.assertIn('Create Post', self.browser.title)
