from django import forms
from feed.models import Item

EMPTY_ITEM_ERROR = "You cannot have an empty list item"

class ItemForm(forms.models.ModelForm):
	
	class Meta:
		model = Item
		fields = ('text',)
		widgets = {
			'text': forms.fields.TextInput(
					attrs={
						'placeholder': 'What you are selling',
						'class': 'form-control input-lg'
					})
		}
		error_messages = {
			'text': {'required': EMPTY_ITEM_ERROR}
		}
