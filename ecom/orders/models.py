from django.db import models
from core.models import BaseModel
from product.models import Product
from customers.models import Customer,Address
from django.utils.translation import gettext_lazy as _
class DiscountCode(BaseModel):
    DISCOUNT_TYPES = [
        ('PG', 'Percentage'),
        ('FA', 'Fixed Amount'),
    ]
    code = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    amount = models.IntegerField()
    max_amount = models.IntegerField(null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    usage_limit = models.PositiveIntegerField()

    def str(self):
        return self.code

class Order(BaseModel):
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELED = 'canceled'

    STATUS_CHOICES = [
        (PENDING, _('Pending')),
        (COMPLETED, _('Completed')),
        (CANCELED, _('Canceled')),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING,
        help_text=_('Status of the order'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.IntegerField()

    def __str__(self):
        return  f"Order {self.id} - {self.get_status_display()}"
    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.IntegerField()
    discount_amount = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order #{self.order.id})"

class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.customer}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Cart of {self.cart.customer})"