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
	return redirect('/feed/one-list/')	

def view_list(request):
	items = Item.objects.all()
	return render(request, 'list.html', {'items': items})