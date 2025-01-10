from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Product, Category, Discount, ProductFeature
from .serializers import ProductSerializer, CategorySerializer, DiscountSerializer, ProductFeatureSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.prefetch_related('discounts').select_related('category')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'brand']
    search_fields = ['name', 'description']

    @action(detail=False, methods=['get'], url_path='discounted')
    def discounted_products(self, request):
        discounted_products = self.queryset.filter(discounts__isnull=False)
        serializer = self.get_serializer(discounted_products, many=True)
        return Response(serializer.data)
    
class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class DiscountViewSet(ReadOnlyModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer

class ProductFeatureViewSet(ReadOnlyModelViewSet):
    queryset = ProductFeature.objects.all()
    serializer_class = ProductFeatureSerializer
