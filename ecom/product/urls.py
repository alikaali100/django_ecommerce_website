from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='products/lsit.html'), name='products'),  # لیست محصولات
    path('<int:id>/', TemplateView.as_view(template_name='products/detail.html'), name='product_detail'),  # جزئیات محصول
]
