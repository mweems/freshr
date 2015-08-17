from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import sys
import time


class ItemValidationTest(FunctionalTest):

	def test_cannot_add_empty_list_items(self):

		self.browser.get(self.server_url)
		self.go_to_sell_page()
		self.get_item_input_box().send_keys('\n')

		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, "You cannot have an empty list item")

		self.get_item_input_box().send_keys("20lbs Ahi\n")
		self.check_for_row_in_list_table("20lbs Ahi")

		self.browser.find_element_by_id('item_text').send_keys('\n')

		self.check_for_row_in_list_table('20lbs Ahi')
		error = self.browser.find_element_by_css_selector('.has-error')
		self.assertEqual(error.text, "You cannot have an empty list item")

		self.self.get_item_input_box().send_keys('10lbs BlueFin Tuna\n')
		self.check_for_row_in_list_table('20lbs Ahi')
		self.check_for_row_in_list_table('10lbs BlueFin Tuna')
