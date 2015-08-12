from selenium import webdriver
import unittest

class NewFishermanTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def test_can_choose_to_sell_or_buy_fish(self):
		self.browser.get('http://localhost:8000')
		self.assertIn('Freshr', self.browser.title)

		self.fail('Finish the test!')

	
if __name__ == '__main__':
	unittest.main(warnings='ignore')
