from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import sys
import time


class ItemValidationTest(FunctionalTest):

	@skip
	def test_cannot_add_empty_list_items(self):

		self.fail('write me!')
