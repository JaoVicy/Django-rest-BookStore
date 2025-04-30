import pytest
from decimal import Decimal
from product.models.product import Product
from product.models.category import Category
from product.serializers.product_serializer import ProductSerializer
import uuid  # Importar uuid para gerar slugs únicos


@pytest.mark.django_db
class TestProductSerializer:

    def test_product_serializer_valid_data(self):
        # Limpar todas as categorias para evitar conflitos de unicidade
        Category.objects.all().delete()

        # Gerar um slug único
        unique_slug = f"fiction-{uuid.uuid4()}"

        # Criar uma categoria com um slug único
        category = Category.objects.create(
            title="Fiction",
            slug=unique_slug,
            description="Fiction books",
            active=True
        )

        # Dados do produto a serem testados
        product_data = {
            'title': 'Book Title',
            'description': 'Book Description',
            'price': '19.99',
            'active': True,
            'categories_id': [category.id]  # Usar ID da categoria
        }

        # Serializar os dados do produto
        serializer = ProductSerializer(data=product_data)
        is_valid = serializer.is_valid()

        # Imprimir erros se o serializer não for válido
        if not is_valid:
            print(serializer.errors)

        # Verificar se o serializer é válido
        assert is_valid

        # Salvar o produto e verificar os atributos
        product = serializer.save()
        assert product.title == 'Book Title'
        assert product.description == 'Book Description'
        assert product.price == Decimal('19.99')
        assert product.active is True
        assert product.category.count() == 1
        assert product.category.first().title == 'Fiction'

    def test_product_serializer_invalid_data(self):
        # Dados do produto inválido a serem testados
        product_data = {
            'title': '',
            'description': 'Book Description',
            'price': '19.99',
            'active': True,
            'category': []
        }

        # Serializar os dados do produto
        serializer = ProductSerializer(data=product_data)

        # Verificar se o serializer não é válido
        assert not serializer.is_valid()

        # Verificar se o campo 'title' está nos erros do serializer
        assert 'title' in serializer.errors