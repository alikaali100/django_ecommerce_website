from rest_framework import generics,filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product,Category,Discount
from .serializers import ProductSerializer,CategorySerializer,DiscountSerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = None 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'brand'] 
    search_fields = ['name', 'description']

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class DiscountListView(generics.ListAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer

class DiscountDetailView(generics.RetrieveAPIView):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer