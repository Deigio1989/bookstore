from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

import json

from django.urls import reverse


from product.factories import CategoryFactory, ProductFactory
from order.factories import OrderFactory, UserFactory
from order.models import Order
from product.models import Product


#


class TestProductViewSet(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        token = Token.objects.create(user=self.user)
        token.save()

        self.category = CategoryFactory(title="technology")
        self.product = ProductFactory(
            title="mouse", price=100, category=[self.category], active=True
        )

    def test_get_all_products(self):
        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.get(reverse("product-list", kwargs={"version": "v1"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)
        product_data = data["results"][0]  # Acessar a chave 'results' da paginação
        self.assertEqual(product_data["title"], self.product.title)
        self.assertEqual(product_data["price"], self.product.price)
        self.assertEqual(product_data["active"], self.product.active)

        category_data = product_data["category"]
        self.assertIsInstance(category_data, list)
        self.assertEqual(category_data[0]["title"], self.category.title)

    def test_create_product(self):
        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        category = CategoryFactory()
        data = json.dumps(
            {
                "title": "notebook",
                "price": 800.00,
                "categories_id": [
                    category.id
                ],  # Certifique-se de que a chave é a mesma usada no serializador
            }
        )

        response = self.client.post(
            reverse("product-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )
        if response.status_code != status.HTTP_201_CREATED:
            print(response.content)  # Adicionando depuração para ver a mensagem de erro

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_product = Product.objects.get(title="notebook")
        self.assertEqual(created_product.title, "notebook")
        self.assertEqual(created_product.price, 800.00)
        self.assertIn(category, created_product.category.all())
