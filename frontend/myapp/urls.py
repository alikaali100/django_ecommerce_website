from django.urls import path
from .views import products_view, home_view, contact_view, login_view, register_view, logout_view, product_detail_view, search_products_view, cart_view,remove_from_cart_view

urlpatterns = [
    path('products/', products_view, name='products'),
    path('home/', home_view, name='home'),
    path('contact/', contact_view, name='contact'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name = 'logout'),
    path('products/<int:product_id>/',product_detail_view, name='product_detail'),
    path('search/', search_products_view, name='search_products'),
    path('cart/', cart_view, name='cart'),
    path('cart/remove/', remove_from_cart_view, name='remove_from_cart'),
    # path('user_panel/',)

]
