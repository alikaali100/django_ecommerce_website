from django.urls import path
from .views import AddToCartAPIView,CartAPIView, RemoveFromCartAPIView, CheckoutAPIView, OrderListAPIView

urlpatterns = [
    path('add/', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('', CartAPIView.as_view(), name='view-cart'),
    path('remove/', RemoveFromCartAPIView.as_view(), name='remove-from-cart'),
    path('checkout/', CheckoutAPIView.as_view(), name='checkout'),
    path('orders/', OrderListAPIView.as_view(), name='order-list'),
]