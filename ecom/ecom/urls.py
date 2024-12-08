from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),  
    path('products/', include('product.urls')),  
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),   
    path('cart/', TemplateView.as_view(template_name='cart.html'), name='cart'),  
    path('customers/', include('customers.urls')), 
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),  
    path('faq/', TemplateView.as_view(template_name='faq.html'), name='faq'), 
]
