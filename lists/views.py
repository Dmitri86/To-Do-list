from lists.models import Item
from django.shortcuts import render, redirect
# Create your views here.

def home_page(request):
	'''домашняя страница'''
	return render(request, 'home.html')


def view_list(request):
	'''представление списка'''
	items = Item.objects.all()
	return render(request, 'list.html', {'items': items})

def new_list(request):
	'''новый список'''
	Item.objects.create(text=request.POST['item_text'])
	return redirect(view_list)
