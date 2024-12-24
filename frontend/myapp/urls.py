from django.urls import path
from .views import products_view, signup_view, login_view

urlpatterns = [
    path('products/', products_view, name='products'),
    path('signup/',signup_view, name= 'signup'),
    path('login/', login_view, name='login')
]
