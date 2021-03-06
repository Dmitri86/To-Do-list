from django.core.exceptions import ValidationError
from lists.models import Item, List
from django.shortcuts import render, redirect
# Create your views here.

def home_page(request):
	'''домашняя страница'''
	return render(request, 'home.html')


def view_list(request, list_id):
	'''представление списка'''
	list_ = List.objects.get(id=list_id)
	if request.method == 'POST':
		Item.objects.create(text=request.POST['item_text'], list=list_)
		return redirect(f'/lists/{list_.id}/')
	return render(request, 'list.html', {'list': list_})

def new_list(request):
	'''новый список'''
	list_ = List.objects.create()
	item = Item.objects.create(text=request.POST['item_text'], list=list_)
	try:
		item .full_clean()
		item.save()
	except ValidationError:
		list_.delete()
		error = "You can't have an empty list item"
		return render(request, 'home.html', {"error": error})
	return redirect(f'/lists/{list_.id}/')


