from django.urls import path
from .views import ProductListView, ProductDetailView

urlpatterns = [
    path('api/products/', ProductListView.as_view(), name='product-list'),
    path('api/products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]
