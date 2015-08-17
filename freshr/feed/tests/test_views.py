from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from feed.views import home_page, create_page, feed_page
from feed.models import Item, List
from feed.forms import ItemForm

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
	maxDiff = None

	def test_create_page_renders_create_template(self):
		response = self.client.get('/feed/create')
		self.assertTemplateUsed(response, 'create.html')

	def test_create_page_uses_item_form(self):
		response = self.client.get('/feed/create')
		self.assertIsInstance(response.context['form'], ItemForm)

class NewsFeedPageTest(TestCase):

	def test_news_feed_url_resolves_to_newsfeed_page_view(self):
		found = resolve('/feed/feed')
		self.assertEqual(found.func, feed_page)

	def test_feed_page_returns_correct_html(self):
		request = HttpRequest()
		response = feed_page(request)
		expected_html = render_to_string('feed.html')
		self.assertEqual(response.content.decode(), expected_html)


class ListViewTest(TestCase):

	def test_displays_list_template(self):
		list_ = List.objects.create()
		response = self.client.get('/feed/%d/' % list_.id)
		self.assertTemplateUsed(response, 'list.html')

	def test_displays_only_items_for_that_list(self):
		correct_list = List.objects.create()
		other_list = List.objects.create()

		Item.objects.create(text='itemey 1', list=correct_list)
		Item.objects.create(text='itemey 2', list=correct_list)

		Item.objects.create(text='other list item 1', list=other_list)
		Item.objects.create(text='other list item 2', list=other_list)

		response = self.client.get('/feed/%d/' % correct_list.id)

		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')
		self.assertNotContains(response, 'other list item 1')
		self.assertNotContains(response, 'other list item 2')

	def test_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.get('/feed/%d/' % correct_list.id)
		self.assertEqual(response.context['list'], correct_list)

	def test_can_save_a_post_request_to_an_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		self.client.post(
			'/feed/%d/' % correct_list.id,
			data={'text': 'A new item to an existing list'}
		)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item to an existing list')
		self.assertEqual(new_item.list, correct_list)

	def test_post_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post(
			'/feed/%d/' % correct_list.id,
			data={'text': 'A new item to an existing list'}
		)

		self.assertRedirects(response, '/feed/%d/' % correct_list.id)

	def test_validation_error_end_up_on_lists_page(self):
		list_ = List.objects.create()
		response = self.client.post(
			'/feed/%d/' % list_.id,
			data={'text': ''}
		)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'list.html')
		expected_error = 'You cannot have an empty list item'
		self.assertContains(response, expected_error)

		
class NewListTest(TestCase):

	def test_saving_a_post_request(self):
		self.client.post(
			'/feed/new',
			data={'text': 'A new item'}
			)
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item')

	def test_redirects_after_a_post(self):
		response = self.client.post(
			'/feed/new',
			data={'text': 'A new item'}
			)
		new_list = List.objects.first()
		self.assertRedirects(response, '/feed/%d/' % new_list.id)

	def test_validation_errors_are_sent_back_to_create_page_template(self):
		response = self.client.post('/feed/new', data={'text': ''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'create.html')
		expected_error = "You cannot have an empty list item"
		self.assertContains(response, expected_error)

	def test_invalid_list_items_are_not_saved(self):
		self.client.post(
			'/feed/new', 
			data={'text': ''}
		)
		self.assertEqual(List.objects.count(), 0)
		self.assertEqual(Item.objects.count(), 0)
