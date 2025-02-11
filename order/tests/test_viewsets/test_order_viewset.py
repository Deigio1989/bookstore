from rest_framework.test import APIClient, APITestCase
from rest_framework import status
import json

from django.urls import reverse


from product.factories import CategoryFactory, ProductFactory
from order.factories import OrderFactory, UserFactory
from order.models import Order
from product.models import Product
#

class TestOrderViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title='technology')
        self.product = ProductFactory(title='mouse', price=100, category=[self.category])
        self.order = OrderFactory(product=[self.product])

    
    def test_order(self):
        response = self.client.get(
            reverse('order-list', kwargs={'version': 'v1'})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)[0]
        self.assertEqual(order_data['product'][0]['title'], self.product.title)
        self.assertEqual(order_data['product'][0]['price'], self.product.price)
        self.assertEqual(order_data['product'][0]['active'], self.product.active)

        category_data = order_data['product'][0]['category']
        self.assertIsInstance(category_data, list)
        self.assertEqual(category_data[0]['title'], self.category.title)



    def test_create_order(self):
        user = UserFactory()
        product = ProductFactory()
        data = json.dumps({
            'products_id': [product.id],
            'user': user.id        
        })

        response = self.client.post(
            reverse('order-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )
        if response.status_code != status.HTTP_201_CREATED:
            print(response.content)  # Adicionando depuração para ver a mensagem de erro

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_order = Order.objects.get(user=user)
        self.assertEqual(created_order.user, user)

