from django.db import models
from core.models import BaseModel
from product.models import Product
from customers.models import Customer, Address
from django.utils.translation import gettext_lazy as _

class DiscountCode(BaseModel):
    DISCOUNT_TYPES = [
        ('PG', 'درصدی'),
        ('FA', 'مقدار ثابت'),
    ]
    code = models.CharField(max_length=50, unique=True, verbose_name=_('کد تخفیف'))
    type = models.CharField(max_length=20, choices=DISCOUNT_TYPES, verbose_name=_('نوع تخفیف'))
    amount = models.IntegerField(verbose_name=_('مقدار تخفیف'))
    max_amount = models.IntegerField(null=True, blank=True, verbose_name=_('حداکثر تخفیف'))
    start_date = models.DateTimeField(verbose_name=_('تاریخ شروع'))
    end_date = models.DateTimeField(verbose_name=_('تاریخ پایان'))
    usage_limit = models.PositiveIntegerField(verbose_name=_('محدودیت استفاده'))

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _('کد تخفیف')
        verbose_name_plural = _('کدهای تخفیف')


class Order(BaseModel):
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELED = 'canceled'

    STATUS_CHOICES = [
        (PENDING, _('در انتظار')),
        (COMPLETED, _('تکمیل شده')),
        (CANCELED, _('لغو شده')),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING,
        help_text=_('وضعیت سفارش'),
        verbose_name=_('وضعیت'),
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name=_('مشتری'),
    )
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name=_('آدرس'))
    discount_code = models.ForeignKey(
        DiscountCode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('کد تخفیف'),
    )
    total_amount = models.IntegerField(verbose_name=_('مبلغ کل'))

    def __str__(self):
        return f"Order {self.id} - {self.get_status_display()}"

    class Meta:
        verbose_name = _('سفارش')
        verbose_name_plural = _('سفارش‌ها')


class Cart(models.Model):
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name=_('مشتری'),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاریخ ایجاد'))
    total_price = models.PositiveBigIntegerField(default=0, verbose_name=_('قیمت کل'))

    def __str__(self):
        return f"Cart of {self.customer}"

    class Meta:
        verbose_name = _('سبد خرید')
        verbose_name_plural = _('سبدهای خرید')


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('سبد خرید'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('محصول'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('تعداد'))

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Cart of {self.cart.customer})"

    class Meta:
        verbose_name = _('آیتم سبد خرید')
        verbose_name_plural = _('آیتم‌های سبد خرید')


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('سفارش'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('محصول'))
    quantity = models.PositiveIntegerField(verbose_name=_('تعداد'))
    price = models.PositiveIntegerField(verbose_name=_('قیمت'))
    discount_amount = models.PositiveIntegerField(verbose_name=_('مقدار تخفیف'))

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order #{self.order.id})"

    class Meta:
        verbose_name = _('آیتم سفارش')
        verbose_name_plural = _('آیتم‌های سفارش')
