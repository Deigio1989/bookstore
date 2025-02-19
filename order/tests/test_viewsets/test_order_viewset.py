import json
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from order.factories import OrderFactory, UserFactory
from product.factories import CategoryFactory, ProductFactory
from order.models import Order

class TestOrderViewSet(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.category = CategoryFactory(title='technology')
        self.product = ProductFactory(title='mouse', price=100, category=[self.category])
        self.order = OrderFactory(user=self.user)
        self.order.product.add(self.product)

    def test_order(self):
        response = self.client.get(
            reverse('order-list', kwargs={'version': 'v1'})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        order_data = data['results'][0]
        self.assertEqual(order_data['product'][0]['title'], self.product.title)
        self.assertEqual(order_data['product'][0]['price'], self.product.price)
        self.assertEqual(order_data['product'][0]['active'], self.product.active)

        category_data = order_data['product'][0]['category']
        self.assertIsInstance(category_data, list)
        self.assertEqual(category_data[0]['title'], self.category.title)

    def test_create_order(self):
        data = {
            'user': self.user.id,
            'products_id': [self.product.id],
        }

        response = self.client.post(
            reverse('order-list', kwargs={'version': 'v1'}),
            data=json.dumps(data),
            content_type='application/json'
        )
        if response.status_code != status.HTTP_201_CREATED:
            print(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Adicionar filtro para garantir que estamos obtendo o pedido correto
        created_order = Order.objects.filter(user=self.user, product=self.product).first()
        self.assertIsNotNone(created_order)
        self.assertEqual(created_order.user, self.user)
        self.assertIn(self.product, created_order.product.all())
