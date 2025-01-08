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

from django.http import HttpResponse


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
                "refresh": str(refresh),
            }, status=200)
            response.set_cookie(
                key="access_token",
                value=access_token,
                max_age=3600,
                samesite='Lax',
            )
            return response
        
        return Response({"error": "Invalid credentials."}, status=401)
    
class SendOTPView(APIView):
    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                # Try to fetch the customer by email
                customer = Customer.objects.get(email=email)
                
                # Generate OTP for the customer
                customer.generate_otp()

                # Send OTP via email
                send_mail(
                    subject="Your OTP Code",
                    message=f"Your OTP code is {customer.otp}. It is valid for 5 minutes.",
                    from_email="noreply@example.com",
                    recipient_list=[customer.email],
                )

                return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)
            
            except Customer.DoesNotExist:
                # If customer is not found, return a 404 error
                return Response({"error": "Customer with this email not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ValidateOTPView(APIView):
    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data.get('otp')
            try:
                customer = Customer.objects.get(email=email)
                if customer.otp == otp and now() < customer.otp_expiry:
                    customer.otp = None  # Clear OTP after successful validation
                    customer.otp_expiry = None
                    customer.save()
                    return Response({"message": "OTP validated successfully."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)
            except Customer.DoesNotExist:
                return Response({"error": "Customer with this email not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
