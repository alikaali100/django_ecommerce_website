from django.contrib import admin
from django.urls import path, include  # include برای وارد کردن مسیرهای اپلیکیشن‌ها

urlpatterns = [
    path('admin/', admin.site.urls),  # مسیر مدیریت Django
    path('', include('myapp.urls')),  # مسیرهای اپلیکیشن شما
]
