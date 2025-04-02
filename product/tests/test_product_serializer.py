import pytest
from product.models.product import Product
from product.models.category import Category
from product.serializers.product_serializer import ProductSerializer
from product.serializers.category_serializer import CategorySerializer


@pytest.mark.django_db
class TestProductSerializer:

    def test_product_serializer_valid_data(self):
        category = Category.objects.create(title="Fiction", slug="fiction", description="Fiction books", active=True)
        product_data = {
            'title': 'Book Title',
            'description': 'Book Description',
            'price': '19.99',
            'active': True,
            'category': [CategorySerializer(category).data]
        }
        serializer = ProductSerializer(data=product_data)
        assert serializer.is_valid()
        product = serializer.save()
        assert product.title == 'Book Title'
        assert product.description == 'Book Description'
        assert product.price == 19.99
        assert product.active is True

    def test_product_serializer_invalid_data(self):
        product_data = {
            'title': '',
            'description': 'Book Description',
            'price': '19.99',
            'active': True,
            'category': []
        }
        serializer = ProductSerializer(data=product_data)
        assert not serializer.is_valid()
        assert 'title' in serializer.errors