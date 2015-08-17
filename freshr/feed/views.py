from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from feed.models import Item, List
from feed.forms import ItemForm

def home_page(request):
	return render(request, 'home.html')

def create_page(request):
	return render(request, 'create.html', {'form': ItemForm()})

def feed_page(request):
	return render(request, 'feed.html')

def new_list(request):
	list_ = List.objects.create()
	item = Item.objects.create(text=request.POST['text'], list=list_)
	try:
		item.full_clean()
		item.save()
	except ValidationError:
		list_.delete()
		error = "You cannot have an empty list item"
		return render(request, 'create.html', {'error': error})
	return redirect(list_)	

def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	error = None

	if request.method == 'POST':
		try:
			item = Item.objects.create(text=request.POST['text'], list=list_)
			item.full_clean()
			item.save()
			return redirect(list_)
		except ValidationError:
			error = "You cannot have an empty list item"
	return render(request, 'list.html', {'list': list_, 'error': error})
