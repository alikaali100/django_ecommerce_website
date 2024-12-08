from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('profile/', TemplateView.as_view(template_name='account/profile.html'), name='profile'),  
    path('login/', TemplateView.as_view(template_name='account/login.html'), name='login'),  
    path('logout/', TemplateView.as_view(template_name='account/logout.html'), name='logout'), 
    path('register/', TemplateView.as_view(template_name='account/register.html'), name='register'),  
]
