from django.db import models
from core.models import BaseModel
from django.utils.timezone import now
from rest_framework.response import Response

class Category(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name

class Product(BaseModel):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    brand = models.TextField(max_length=50)
    model = models.TextField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    image = models.URLField(max_length=500, blank=True)
    discounts = models.ManyToManyField('Discount', blank=True, related_name='products')

    def __str__(self):
        return self.name
    @property
    def discounted_price(self):
        # فیلتر تخفیف‌های فعال
        active_discounts = self.discounts.filter(
            start_date__lte=now(),
            end_date__gte=now()
        )

        # محاسبه قیمت نهایی با تخفیف
        final_price = self.price
        for discount in active_discounts:
            if discount.type == 'PG':  # تخفیف درصدی
                discount_amount = self.price * discount.amount / 100
                max_amount = discount.max_amount or float('inf')  # اگر None باشد، بی‌نهایت در نظر گرفته می‌شود
                discount_amount = min(discount_amount, max_amount)
            elif discount.type == 'FA':  # تخفیف مبلغ ثابت
                max_amount = discount.max_amount or discount.amount  # اگر None باشد، برابر با مقدار تخفیف قرار می‌گیرد
                discount_amount = min(discount.amount, max_amount)

            final_price -= discount_amount

        # جلوگیری از منفی شدن قیمت
        return max(final_price, 0)
        
class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features')
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    display_order = models.IntegerField()

    def __str__(self):
        return f"{self.key}: {self.value}"
class Discount(BaseModel):
    DISCOUNT_TYPES = [
        ('PG', 'Percentage'),
        ('FA', 'Fixed Amount'),
    ]
    type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    amount = models.IntegerField()
    max_amount = models.IntegerField(null=True, blank=True, default=None)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.type} - {self.amount}"
