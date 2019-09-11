from django.test import TestCase
from django.http import HttpRequest
from django.urls import resolve
from lists.views import home_page

# Create your tests here.

class HomePageTest(TestCase):
	'''тест домашней страницы'''

	def test_root_url_resolves_to_home_page_view(self):
		'''тест: корневой урл преобразуется в представление домащней страницы'''
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		'''тест: домашняя страница возвращает правильный html'''
		request = HttpRequest()
		response = home_page(request)
		html = response.content.decode('utf-8')
		self.assertTrue(html.startswith('<html>'))
		self.assertIn('<title>TO-DO</title>', html)
		self.assertTrue(html.endswith('</html>'))
