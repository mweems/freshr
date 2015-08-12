from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewFishermanTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_can_choose_to_sell_or_buy_fish(self):
		self.browser.get('http://localhost:8000')
		self.assertIn('Freshr', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('Welcome to Freshr', header_text)

		sell_button = self.browser.find_element_by_id('sell_fish')

		sell_button.send_keys(Keys.ENTER)

		self.fail('Finish the test!')

	
if __name__ == '__main__':
	unittest.main(warnings='ignore')
