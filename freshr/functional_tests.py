from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewFishermanTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_can_choose_to_sell_fish(self):
		self.browser.get('http://localhost:8000')
		self.assertIn('Freshr', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('Welcome to Freshr', header_text)

		sell_button = self.browser.find_element_by_id('sell_fish')
		buy_button = self.browser.find_element_by_id('buy_fish')

		sell_button.send_keys(Keys.ENTER)

		create_post_url = self.browser.current_url
		self.assertRegex(create_post_url, '/create')

	def test_can_create_a_post_and_retrieve_it_later(self):
		self.browser.get('http://localhost:8000/create')
		self.assertIn('Create Post', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h2').text
		self.assertIn('New Post', header_text)
		
		inputBox = self.browser.find_element_by_id('item_text')
		
		self.assertEqual(inputBox.get_attribute('placeholder'), 'What you are selling')
		
		inputBox.send_keys('50lbs Tuna, $5 a pound')
		inputBox.send_keys(Keys.ENTER)

		table = self.browser.find_element_by_id('list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('50lbs Tuna, $5 a pound', [row.text for row in rows])

		inputBox = self.browser.find_element_by_id('item_text')
		inputBox.send_keys('30lbs Ahi, $5 a pound')
		inputBox.send_keys(Keys.ENTER)

		table = self.browser.find_element_by_id('list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('50lbs Tuna, $5 a pound', [row.text for row in rows])
		self.assertIn('30lbs Ahi, $5 a pound', [row.text for row in rows])

		self.fail('Finish the test!')

	
if __name__ == '__main__':
	unittest.main(warnings='ignore')
