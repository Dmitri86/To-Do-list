from django.utils.html import escape
from django.test import TestCase
from django.http import HttpRequest
from django.urls import resolve
from lists.views import home_page
from django.template.loader import render_to_string
from lists.models import Item, List


# Create your tests here.

class HomePageTest(TestCase):
	'''тест домашней страницы'''

	def test_root_url_resolves_to_home_page_view(self):
		'''тест: корневой урл преобразуется в представление домащней страницы'''
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		'''тест: домашняя страница возвращает правильный html'''
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')


class ListViewTest(TestCase):
	'''тест представления списка'''

	def test_uses_list_template(self):
                '''тест: используется шаблон списка'''
                list_ = List.objects.create()
                response = self.client.get(f'/lists/{list_.id}/')
                self.assertTemplateUsed(response, 'list.html')


	def test_displays_only_items_for_that_list(self):
		'''тест: отображаются все элементы списка'''
		correct_list = List.objects.create()
		Item.objects.create(text='itemey 1', list=correct_list)
		Item.objects.create(text='itemey 2', list=correct_list)
		other_list = List.objects.create()
		Item.objects.create(text='другой элемент 1 списка', list=other_list)
		Item.objects.create(text='другой элемент 2 списка', list=other_list)

		response = self.client.get(f'/lists/{correct_list.id}/')

		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')
		
		response = self.client.get(f'/lists/{other_list.id}/')
		self.assertContains(response, 'другой элемент 1 списка')
		self.assertContains(response, 'другой элемент 2 списка')

	def test_passes_correct_list_to_template(self):
		'''тест: передается правильный шаблон списка'''
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.get(f'/lists/{correct_list.id}/')
		self.assertEqual(response.context['list'], correct_list)

	def test_can_save_a_POST_request_to_an_existing_list(self):
		'''тест: можно сохранить post-запрос в существующий список'''
		other_list = List.objects.create()
		correct_list = List.objects.create()

		self.client.post(f'/lists/{correct_list.id}/',
			data={'item_text': 'A new item for an existing list'})

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)
	
	def test_POST_redirects_to_list_view(self):
		'''тест: post-запрос переадресуется в представление списка'''
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post(f'/lists/{correct_list.id}/',
			data={'item_text': 'A new item for an existing list'})
		
		self.assertRedirects(response, f'/lists/{correct_list.id}/')

class NewListTest(TestCase):
	'''тест нового списка'''

	def test_can_save_a_POST_request(self):
		'''тест: можно сохранить post-запрос'''
		self.client.post('/lists/new', data={'item_text': 'A new list item'})
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_redirect_after_POST(self):
		'''тест: пререадресует после post-запроса'''
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
		new_list = List.objects.first()
		self.assertRedirects(response, f'/lists/{new_list.id}/')

	def test_validation_errors_are_sent_back_to_home_page_template(self):
		'''тест: ошибки валидации отсылаются назад в шаблон домашеней страницы'''

		response = self.client.post('/lists/new', data={'item_text': ''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')
		expected_error = escape("You can't have an empty list item")
		self.assertContains(response, expected_error)

	def test_invalid_list_items_arent_saved(self):
		'''тест: сохраняются недоступные элементы списка'''
		self.client.post('/list/new', data={'item_text': ''})
		self.assertEqual(List.objects.count(), 0)
		self.assertEqual(Item.objects.count(), 0)

