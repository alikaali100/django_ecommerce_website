from rest_framework import serializers
from .models import Product,Category,Discount,ProductFeature
from django.utils import timezone

class DiscountSerializer(serializers.ModelSerializer):
    class Meta :
        model = Discount
        fields = ['id', 'type', 'amount', 'max_amount', 'start_date', 'end_date']

class ProductSerializer (serializers.ModelSerializer):
    discounts = DiscountSerializer(many=True)
    # has_discount = serializers.SerializerMethodField()
    # def get_has_discount(self, obj):
    #     now = timezone.now()
    #     return obj.discounts.filter(
    #         start_date__lte=now, end_date__gte=now, is_active=True
    #     ).exists()
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'products']


class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields='__all__'