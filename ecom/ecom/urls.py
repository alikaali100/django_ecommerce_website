from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('product.urls')),
    path('api/customers/', include('customers.urls')),
    path('api/cart/', include('orders.urls'))
]
