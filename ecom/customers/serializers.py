from rest_framework import serializers
from .models import Customer

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'password', 'phone_number']

    def create(self, validated_data):
        customer = Customer(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
        )
        customer.set_password(validated_data['password'])
        customer.save()
        return customer
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
