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
		
		nameInputBox = self.browser.find_element_by_id('name')
		phoneInputBox = self.browser.find_element_by_id('phone')
		inputBox = self.browser.find_element_by_id('new_item')
		submitButton = self.browser.find_element_by_tag_name('button')
		
		self.assertEqual(nameInputBox.get_attribute('placeholder'), 'Your Name')
		self.assertEqual(phoneInputBox.get_attribute('placeholder'), 'Your Phone Number')
		self.assertEqual(inputBox.get_attribute('placeholder'), 'What you are selling')
		
		nameInputBox.send_keys('Paula')
		phoneInputBox.send_keys('808-452-9509')
		inputBox.send_keys('50lbs Tuna, $5 a pound')
		submitButton.send_keys(Keys.ENTER)

		table = self.browser.find_element_by_id('list_table')
		rows = table.find_element_by_tag_name('tr')
		self.assertTrue(any(row.text == 'Paula' for row in rows))
		self.assertTrue(any(row.text == '808-452-9509' for row in rows))
		self.assertTrue(any(row.text == '50lbs Tuna, $5 a pound' for row in rows))

		self.fail('Finish the test!')

	
if __name__ == '__main__':
	unittest.main(warnings='ignore')
