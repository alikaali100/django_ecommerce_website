from django.urls import path
from .views import ProductListView, ProductDetailView,CategoryListView,CategoryDetailView,DiscountListView,DiscountDetailView

urlpatterns = [
    path('api/products/', ProductListView.as_view(), name='product-list'),
    path('api/products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('api/categories/', CategoryListView.as_view(), name='category-list'),
    path('api/categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('api/discounts/', DiscountListView.as_view(), name='discount-list'),
    path('api/discounts/<int:pk>/', DiscountDetailView.as_view(), name='discount-detail'),
]
