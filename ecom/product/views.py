from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Product, Category, Discount, ProductFeature
from .serializers import ProductSerializer, CategorySerializer, DiscountSerializer, ProductFeatureSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404


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


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.prefetch_related('subcategories').all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']

    def get_queryset(self):
        parent_id = self.request.query_params.get('parent')
        if parent_id:
            return self.queryset.filter(parent_id=parent_id)
        return self.queryset.filter(subcategories__isnull=False).distinct()
    
    @action(detail=True, methods=['get'], url_path='products')
    def products(self, request, pk=None):
        """
        اکشن سفارشی برای دریافت محصولات مرتبط با یک دسته‌بندی
        """
        category = get_object_or_404(Category, pk=pk)  # پیدا کردن دسته‌بندی بر اساس `pk`
        products = Product.objects.filter(category=category)  # فیلتر محصولات مرتبط
        serializer = ProductSerializer(products, many=True)  # سریالایز کردن لیست محصولات
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='root-categories')
    def root_categories(self, request):
        """
        اکشن سفارشی برای دریافت دسته‌بندی‌های والد
        """
        root_categories = self.queryset.filter(parent__isnull=True)
        serializer = self.get_serializer(root_categories, many=True)
        return Response(serializer.data)


class DiscountViewSet(ReadOnlyModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


class ProductFeatureViewSet(ReadOnlyModelViewSet):
    queryset = ProductFeature.objects.all()
    serializer_class = ProductFeatureSerializer
