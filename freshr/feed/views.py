from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from feed.models import Item, List

def home_page(request):
	return render(request, 'home.html')

def create_page(request):
	return render(request, 'create.html')

def new_list(request):
	list_ = List.objects.create()
	item = Item.objects.create(text=request.POST['item_text'], list=list_)
	try:
		item.full_clean()
		item.save()
	except ValidationError:
		list_.delete()
		error = "You cannot have an empty list item"
		return render(request, 'create.html', {'error': error})
	return redirect('/feed/%d/' % list_.id)	

def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	if request.method == 'POST':
		Item.objects.create(text=request.POST['item_text'], list=list_)
		return redirect('/feed/%d/' % list_.id)
	return render(request, 'list.html', {'list': list_})
