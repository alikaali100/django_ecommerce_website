from django.db import models
from core.models import BaseModel
from django.utils.timezone import now
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
class Category(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_('نام دسته‌بندی'))
    description = models.TextField(blank=True, null=True, verbose_name=_('توضیحات'))
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name=_('دسته‌بندی والد')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('دسته‌بندی')
        verbose_name_plural = _('دسته‌بندی‌ها')

class Product(BaseModel):
    name = models.CharField(max_length=50, verbose_name=_('نام محصول'))
    description = models.TextField(max_length=250, verbose_name=_('توضیحات'))
    price = models.PositiveIntegerField(verbose_name=_('قیمت'))
    stock = models.PositiveIntegerField(verbose_name=_('موجودی'))
    brand = models.TextField(max_length=50, verbose_name=_('برند'))
    model = models.TextField(max_length=50, verbose_name=_('مدل'))
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
        verbose_name=_('دسته‌بندی')
    )
    image = models.URLField(max_length=500, blank=True, verbose_name=_('تصویر'))
    discounts = models.ManyToManyField(
        'Discount',
        blank=True,
        related_name='products',
        verbose_name=_('تخفیف‌ها')
    )

    def __str__(self):
        return self.name

    @property
    def discounted_price(self):
        active_discounts = self.discounts.filter(
            start_date__lte=now(),
            end_date__gte=now()
        )

        final_price = self.price
        for discount in active_discounts:
            if discount.type == 'PG':  
                discount_amount = self.price * discount.amount / 100
                max_amount = discount.max_amount or float('inf')  
                discount_amount = min(discount_amount, max_amount)
            elif discount.type == 'FA':
                max_amount = discount.max_amount or discount.amount 
                discount_amount = min(discount.amount, max_amount)
            final_price -= discount_amount
        return max(int(final_price), 0) 

    class Meta:
        verbose_name = _('محصول')
        verbose_name_plural = _('محصولات')

class ProductFeature(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='features',
        verbose_name=_('محصول')
    )
    key = models.CharField(max_length=50, verbose_name=_('ویژگی'))
    value = models.CharField(max_length=50, verbose_name=_('مقدار'))
    display_order = models.IntegerField(verbose_name=_('ترتیب نمایش'))

    def __str__(self):
        return f"{self.key}: {self.value}"

    class Meta:
        verbose_name = _('ویژگی محصول')
        verbose_name_plural = _('ویژگی‌های محصول')
class Discount(BaseModel):
    DISCOUNT_TYPES = [
        ('PG', _('درصدی')),
        ('FA', _('مقدار ثابت')),
    ]
    type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPES,
        verbose_name=_('نوع تخفیف')
    )
    amount = models.IntegerField(verbose_name=_('مقدار تخفیف'))
    max_amount = models.IntegerField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_('حداکثر تخفیف')
    )
    start_date = models.DateTimeField(verbose_name=_('تاریخ شروع'))
    end_date = models.DateTimeField(verbose_name=_('تاریخ پایان'))

    def __str__(self):
        return f"{self.get_type_display()} - {self.amount}"

    class Meta:
        verbose_name = _('تخفیف')
        verbose_name_plural = _('تخفیف‌ها')