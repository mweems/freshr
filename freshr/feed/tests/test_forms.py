from django.test import TestCase
from feed.forms import ItemForm, EMPTY_ITEM_ERROR

class ItemFormTest(TestCase):

	def test_form_renders_item_text_input(self):
		form = ItemForm()
		self.assertIn('placeholder="What you are selling"', form.as_p())
		self.assertIn('class="form-control input-lg"', form.as_p())

	def test_form_validation_for_blank_items(self):
		form = ItemForm(data={'text': ''})
		self.assertFalse(form.is_valid())
		self.assertEqual(
			form.errors['text'],
			[EMPTY_ITEM_ERROR])
