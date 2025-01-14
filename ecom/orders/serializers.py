from rest_framework import serializers
from .models import CartItem ,Order, OrderItem

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    product_price = serializers.IntegerField(source='product.price')

    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)  # بدون نیاز به 'source'
    address = serializers.CharField(source='address.__str__')  # آدرس به صورت رشته
    discount_code = serializers.CharField(source='discount_code.code', required=False)

    class Meta:
        model = Order
        fields = ['id', 'status', 'total_amount', 'address', 'discount_code', 'created_at', 'items']
