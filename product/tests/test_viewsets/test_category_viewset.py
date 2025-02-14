import json
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from product.factories import CategoryFactory
from product.models import Category
from order.factories import UserFactory

class CategoryViewSetTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.category = CategoryFactory(title='books')

    def test_get_all_category(self):
        response = self.client.get(
            reverse('category-list', kwargs={'version': 'v1'})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        category_data = data['results'][0]
        self.assertEqual(category_data['title'], self.category.title)

    def test_create_category(self):
        data = {
            'title': 'technology'
        }
        response = self.client.post(
            reverse('category-list', kwargs={'version': 'v1'}),
            data=json.dumps(data),
            content_type='application/json'
        )
        if response.status_code != status.HTTP_201_CREATED:
            print(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_category = Category.objects.get(title='technology')
        self.assertEqual(created_category.title, 'technology')
