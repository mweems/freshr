from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from feed.views import home_page, create_page

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)

class CreatePostPageTest(TestCase):

	def test_create_url_resolves_to_create_page_view(self):
		found = resolve('/create')
		self.assertEqual(found.func, create_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = create_page(request)
		expected_html = render_to_string('create.html')
		self.assertEqual(response.content.decode(), expected_html)

	def test_home_page_can_save_a_post_request(self):
		request = HttpRequest()
		request.method = 'Post'
		request.POST['item_text'] = 'A new item'

		response = create_page(request)

		self.assertIn('A new item', response.content.decode())
		
