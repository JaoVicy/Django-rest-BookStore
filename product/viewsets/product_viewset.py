from rest_framework.permissions import IsAuthenticated
from product.models import Product
from product.serializers import ProductSerializer
from rest_framework.viewsets import ModelViewSet


class ProductViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):  # queryset is a method
        return Product.objects.all().order_by("id")
