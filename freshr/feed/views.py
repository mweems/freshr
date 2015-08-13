from django.shortcuts import render, redirect
from django.http import HttpResponse
from feed.models import Item

def home_page(request):
	return render(request, 'home.html')

def create_page(request):
	return render(request, 'create.html')

def new_list(request):
	Item.objects.create(text=request.POST['item_text'])
	return redirect('/feed/one-list/')	

def view_list(request):
	items = Item.objects.all()
	return render(request, 'list.html', {'items': items})