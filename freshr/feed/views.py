from django.shortcuts import render, redirect
from django.http import HttpResponse
from feed.models import Item, List

def home_page(request):
	return render(request, 'home.html')

def create_page(request):
	return render(request, 'create.html')

def new_list(request):
	list_ = List.objects.create()
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect('/feed/%d/' % list_.id)	

def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	return render(request, 'list.html', {'list': list_})

def add_item(request, list_id):
	list_ = List.objects.get(id=list_id)
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect('/feed/%d/' % list_.id)
