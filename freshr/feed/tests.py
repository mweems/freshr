from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from feed.views import home_page, create_page
from feed.models import Item, List

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

class ListAndItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		list_ = List()
		list_.save()
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.list = list_
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.list = list_
		second_item.save()

		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(first_saved_item.list, list_)
		self.assertEqual(second_saved_item.text, 'Item the second')
		self.assertEqual(second_saved_item.list, list_)

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
		new_list = List.objects.first()
		self.assertRedirects(response, '/feed/%d/' % new_list.id)

class NewItemTest(TestCase):

	def test_can_save_a_post_request_to_an_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		self.client.post(
			'/feed/%d/add_item' % correct_list.id,
			data={'item_text': 'A new item to an existing list'}
		)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item to an existing list')
		self.assertEqual(new_item.list, correct_list)

	def test_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post(
			'/feed/%d/add_item' % correct_list.id,
			data={'item_text': 'A new item to an existing list'}
		)

		self.assertRedirects(response, '/feed/%d/' % correct_list.id)

		
