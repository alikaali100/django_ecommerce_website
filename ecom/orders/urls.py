from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('checkout/', TemplateView.as_view(template_name='checkout.html'), name='order-checkout'),
]
