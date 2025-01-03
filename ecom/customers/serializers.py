from rest_framework import serializers
from .models import Customer
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'username', 'email', 'password']
class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(required=False)