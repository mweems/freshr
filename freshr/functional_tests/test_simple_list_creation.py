from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import sys
import time

class NewFishermanTest(FunctionalTest):


	def test_can_choose_to_sell_fish(self):
		self.browser.get(self.server_url)
		self.assertIn('Freshr', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('Welcome to Freshr', header_text)

		sell_button = self.browser.find_element_by_id('sell_fish')
		buy_button = self.browser.find_element_by_id('buy_fish')

		sell_button.send_keys(Keys.ENTER)

		create_post_url = self.browser.current_url
		self.assertRegex(create_post_url, '/feed/create')

	def test_can_create_a_post_and_retrieve_it_later(self):
		self.browser.get(self.server_url)
		self.go_to_sell_page()
		header_text = self.browser.find_element_by_tag_name('h2').text
		
		inputBox = self.get_item_input_box()
		
		self.assertEqual(inputBox.get_attribute('placeholder'), 'What you are selling')
		
		inputBox.send_keys('50lbs Tuna, $5 a pound')
		inputBox.send_keys(Keys.ENTER)
		first_list_url = self.browser.current_url
		self.assertRegex(first_list_url, '/feed/.+')

		self.check_for_row_in_list_table('50lbs Tuna, $5 a pound')

		inputBox = self.get_item_input_box()
		inputBox.send_keys('30lbs Ahi, $5 a pound')
		inputBox.send_keys(Keys.ENTER)

		self.check_for_row_in_list_table('50lbs Tuna, $5 a pound')
		self.check_for_row_in_list_table('30lbs Ahi, $5 a pound')

		self.browser.quit()
		self.browser = webdriver.Firefox()

		self.browser.get(self.server_url)
		self.go_to_sell_page()
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('50lbs Tuna', page_text)
		self.assertNotIn('30lbs Ahi', page_text)

		inputBox = self.get_item_input_box()
		inputBox.send_keys('Mackeral 20lbs, $2 a pound')
		inputBox.send_keys(Keys.ENTER)

		second_list_url = self.browser.current_url
		self.assertRegex(second_list_url, '/feed/.+')
		self.assertNotEqual(second_list_url, first_list_url)

		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('50lbs Tuna', page_text)
		self.assertIn('Mackeral 20lbs, $2 a pound', page_text)
