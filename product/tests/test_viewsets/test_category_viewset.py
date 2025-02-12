import json

from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

from django.urls import reverse

from product.factories import CategoryFactory
from product.models import Category

class CategoryViewSet(APITestCase):
    client = APIClient

    def setUp(self):
        self.category = CategoryFactory(title='books')
        

    def test_get_all_category(self):
        response = self.client.get(
            reverse('category-list', kwargs={'version': 'v1'})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        category_data = data['results'][0]  # Acessar a chave 'results' da paginação
        self.assertEqual(category_data['title'], self.category.title)



    def test_create_category(self):
        data = json.dumps({
            'title': 'technology'
        })

        response = self.client.post(
            reverse('category-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )
        if response.status_code != status.HTTP_201_CREATED:
            print(response.content)  # Adicionando depuração para ver a mensagem de erro

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_category = Category.objects.get(title='technology')

        self.assertEqual(created_category.title, 'technology')
      
   

