from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from .models import Customer
from .serializers import CustomerSerializer, OTPSerializer
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from django.utils.http import http_date
from datetime import timedelta,datetime
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.cache import cache

class RegisterView(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])  # Hash the password
            user.save()
            return Response({"message": "Registration successful."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=400)

        # Fetch user by email and check the password manually
        user = Customer.objects.filter(email=email).first()
        
        if user and check_password(password, user.password):  # Validate the password
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Create a response and set the cookie
            response = Response({
                "access": access_token,  # Include access token in response
            }, status=200)
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,  # Ensure cookie cannot be accessed via JavaScript
                max_age=3600,  # Cookie expiration in seconds
                samesite='Lax',
                secure=True,  # Use only with HTTPS in production
            )
            return response
        
        return Response({"error": "Invalid credentials."}, status=401)
    
class SendOTPView(APIView):
    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                # بررسی وجود کاربر
                customer = Customer.objects.get(email=email)
                
                # تولید OTP
                import random
                otp = str(random.randint(100000, 999999))
                
                # ذخیره OTP در Redis با انقضای 5 دقیقه
                cache.set(f"otp:{email}", otp, timeout=300)
                
                # ارسال OTP از طریق ایمیل
                send_mail(
                    subject="Your OTP Code",
                    message=f"Your OTP code is {otp}. It is valid for 5 minutes.",
                    from_email="alikaali1990@gmail.com",
                    recipient_list=[customer.email],
                )

                return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)
            
            except Customer.DoesNotExist:
                return Response({"error": "Customer with this email not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ValidateOTPView(APIView):
    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data.get('otp')
            
            cached_otp = cache.get(f"otp:{email}")
            if cached_otp is None:
                return Response({"error": "OTP has expired or does not exist."}, status=status.HTTP_400_BAD_REQUEST)
            
            if cached_otp == otp:
                cache.delete(f"otp:{email}")
                customer = Customer.objects.get(email=email)
                refresh = RefreshToken.for_user(customer)
                access_token = str(refresh.access_token)

                return Response({
                    "message": "OTP validated successfully.",
                    "access": access_token,
                    "refresh": str(refresh)
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Successfully logged out."}, status=200)
        response.delete_cookie("access_token")  # حذف کوکی access_token
        return response
        
class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "phonenumber": user.phone_number,
        })
    
