from django.test import TestCase
from django.urls import reverse

from products.models import Product


class IndexViewTest(TestCase):
    path = reverse('index')

    def test_index_view_status_code(self):
        response = self.client.get(path=self.path)

        self.assertEqual(
            first=response.status_code,
            second=200,
            msg=f'Expected status code is 200, actual is {response.status_code}'
        )

    def test_index_view_title(self):
        response = self.client.get(path=self.path)

        self.assertEqual(
            first=response.context_data['title'],
            second='Store',
            msg=f'Expected title is Store, actual is {response.context_data["title"]}'
        )

    def test_index_view_template_used(self):
        response = self.client.get(path=self.path)

        self.assertTemplateUsed(
            response=response,
            template_name='products/index.html',
            msg_prefix='Unexpected template is used'
        )


class ProductViewTest(TestCase):
    path = reverse('products:index')
    fixtures = ['categories.json', 'goods.json', 'users.json']

    def test_product_view_status_code(self):
        response = self.client.get(path=self.path)

        self.assertEqual(
            first=response.status_code,
            second=200,
            msg=f'Expected status code is 200, actual is {response.status_code}'
        )

    def test_product_view_title(self):
        response = self.client.get(path=self.path)

        self.assertEqual(
            first=response.context_data['title'],
            second='Store - Каталог',
            msg=f'Expected title is Store, actual is {response.context_data["title"]}'
        )

    def test_product_view_template_used(self):
        response = self.client.get(path=self.path)

        self.assertTemplateUsed(
            response=response,
            template_name='products/products.html'
        )

    def test_product_view_query_set(self):
        response = self.client.get(path=self.path)

        self.assertEqual(
            first=list(response.context_data['object_list']),
            second=list(Product.objects.all()[:3]),
            msg='Unexpected products on the page'
        )
