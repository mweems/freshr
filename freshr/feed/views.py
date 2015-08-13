from django.shortcuts import render, redirect
from django.http import HttpResponse
from feed.models import Item

def home_page(request):
	return render(request, 'home.html')

def create_page(request):
	if request.method == 'POST':
		Item.objects.create(text=request.POST['item_text'])
		return redirect('/create')
	items = Item.objects.all()
	return render(request, 'create.html', {'items': items})
