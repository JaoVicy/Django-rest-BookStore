import pytest
from product.models.product import Product

@pytest.mark.django_db
def test_product_creation():
    product = Product.objects.create(title="Test Product", description="Test Description", price=9.99, active=True)
    assert product.title == "Test Product"