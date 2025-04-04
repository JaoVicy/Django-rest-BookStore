from rest_framework import serializers

from product.models.product import Product
from product.models.category import Category
from product.serializers.category_serializer import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True
    )

    class Meta:
        model = Product
        fields = ['title',
                  'description',
                  'price',
                  'active',
                  'category',
                  ]