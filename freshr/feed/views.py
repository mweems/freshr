from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
	return render(request, 'home.html')

def create_page(request):
	return render(request, 'create.html', {
		'new_item_text': request.POST.get('item_text', '')
		})