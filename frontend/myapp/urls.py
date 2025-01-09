from django.urls import path
from .views import products_view, home_view, contact_view, login_view, register_view, logout_view

urlpatterns = [
    path('products/', products_view, name='products'),
    path('home/', home_view, name='home'),
    path('contact/', contact_view, name='contact'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name = 'logout'),
    # path('user_panel/',)

]
