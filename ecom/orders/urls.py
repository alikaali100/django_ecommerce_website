from django.urls import path
from .views import AddToCartAPIView,CartAPIView, RemoveFromCartAPIView, UpdateCartItemAPIView,CheckoutAPIView

urlpatterns = [
    path('add/', AddToCartAPIView.as_view(), name='add-to-cart'),
    path('', CartAPIView.as_view(), name='view-cart'),
    path('remove/', RemoveFromCartAPIView.as_view(), name='remove-from-cart'),
    path('update/', UpdateCartItemAPIView.as_view(), name='update-cart-item'),
    path('checkout/', CheckoutAPIView.as_view(), name='checkout'),
]