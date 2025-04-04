import pytest
from django.contrib.auth.models import User
from product.models.product import Product
from order.models.order import Order
from django.db.utils import IntegrityError


@pytest.mark.django_db
class TestOrderModel:

    def test_order_creation(self):
        # Criação de um usuário
        user = User.objects.create_user(username='testuser', password='12345')

        # Criação de produtos
        product1 = Product.objects.create(title='Product 1', description='Description 1', price=10.0, active=True)
        product2 = Product.objects.create(title='Product 2', description='Description 2', price=20.0, active=True)

        # Criação de um pedido
        order = Order.objects.create(user=user)
        order.product.set([product1, product2])

        # Verificação se o pedido foi criado corretamente
        assert order.user == user
        assert order.product.count() == 2
        assert product1 in order.product.all()
        assert product2 in order.product.all()

    def test_order_without_user(self):
        # Tentativa de criação de um pedido sem usuário
        with pytest.raises(IntegrityError):
            Order.objects.create(user=None)