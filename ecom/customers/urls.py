from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SendOTPView, ValidateOTPView,LoginView,RegisterView,LogoutView,UserProfileView

urlpatterns = [
    path('send_otp/', SendOTPView.as_view(), name='send_otp'),
    path('validate_otp/', ValidateOTPView.as_view(), name='validate_otp'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserProfileView.as_view(), name='user-profile' )
]
