from rest_framework import serializers
from .models import Product,Category,Discount

class ProductSerializer (serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'products']

class DiscountSerializer(serializers.ModelSerializer):
    class Meta :
        model = Discount
        field = '__all__'