import json

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from django.urls import reverse

from product.factories import ProductFactory, CategoryFactory
from order.factories import OrderFactory, UserFactory
from product.models import Product
from order.models import Order


class TestOrderViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        token = Token.objects.create(user=self.user)  # added
        token.save()  # added

        # Garantir que o slug seja único e gerado corretamente
        self.category = CategoryFactory(title="technology", slug="technology-1")
        self.product = ProductFactory(
            title="mouse", price=100, category=[self.category]
        )
        self.order = OrderFactory()  # Cria um pedido com o usuário padrão
        self.order.product.set(
            [self.product]
        )  # Uso do metodo set() para associar o produto ao pedido, evitando o erro de ManyToManyField

    def test_order(self):
        token = Token.objects.get(user__username=self.user.username)  # added
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)  # added
        response = self.client.get(reverse("order-list", kwargs={"version": "v1"}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_data = json.loads(response.content)
        self.assertEqual(
            order_data["results"][0]["product"][0]["title"], self.product.title
        )
        self.assertEqual(
            float(order_data["results"][0]["product"][0]["price"]), self.product.price
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["active"], self.product.active
        )
        self.assertEqual(
            order_data["results"][0]["product"][0]["category"][0]["title"],
            self.category.title,
        )

    def test_create_order(self):
        token = Token.objects.get(user__username=self.user.username)  # added
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)  # added
        user = UserFactory()
        product = ProductFactory()

        # Autentica o client com o usuário criado
        self.client.force_authenticate(user=user)

        data = json.dumps({"products_id": [product.id]})

        response = self.client.post(
            reverse("order-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )
        print("Resposta da API:", response.content)  # <-- Esse é o debug que citei

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(Order.objects.get(id=2).user, user)
