from django.db import models
from core.models import BaseModel

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
    max_amount = models.IntegerField(null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.type} - {self.amount}"
