import pytest
from product.models import Category
from product.serializers import CategorySerializer

@pytest.mark.django_db
class TestCategorySerializer:
    def test_category_serializer_valid_data(self):
        category_data = {
            'title': 'Fiction',
            'slug': 'fiction',
            'description': 'Fiction books',
            'active': True
        }
        serializer = CategorySerializer(data=category_data)
        assert serializer.is_valid()
        category = serializer.save()
        assert category.title == 'Fiction'
        assert category.slug == 'fiction'
        assert category.description == 'Fiction books'
        assert category.active is True

    def test_category_serializer_invalid_data(self):
        category_data = {
            'title': '',
            'slug': 'fiction',
            'description': 'Fiction books',
            'active': True
        }
        serializer = CategorySerializer(data=category_data)
        assert not serializer.is_valid()
        assert 'title' in serializer.errors