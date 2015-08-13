from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from feed.views import home_page, create_page
from feed.models import Item

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

	def test_create_page_returns_correct_html(self):
		request = HttpRequest()
		response = create_page(request)
		expected_html = render_to_string('create.html')
		self.assertEqual(response.content.decode(), expected_html)

	def test_create_page_only_saves_items_when_necessary(self):
		request = HttpRequest()
		create_page(request)
		self.assertEqual(Item.objects.count(), 0)


class ItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(second_saved_item.text, 'Item the second')

class ListViewTest(TestCase):

	def test_displays_list_template(self):
		response = self.client.get('/feed/one-list/')
		self.assertTemplateUsed(response, 'list.html')

	def test_displays_all_items(self):
		Item.objects.create(text='itemey 1')
		Item.objects.create(text='itemey 2')
		response = self.client.get('/feed/one-list/')
		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')

class NewListTest(TestCase):

	def test_saving_a_post_request(self):
		self.client.post(
			'/feed/new',
			data={'item_text': 'A new item'}
			)
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item')

	def test_redirects_after_a_post(self):
		response = self.client.post(
			'/feed/new',
			data={'item_text': 'A new item'}
			)
		self.assertRedirects(response, '/feed/one-list/')

		
