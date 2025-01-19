from django.contrib import admin
from .models import DiscountCode, Order, OrderItem, Cart
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'type', 'amount', 'max_amount', 'start_date', 'end_date', 'usage_limit')
    list_filter = ('type', 'start_date', 'end_date')
    search_fields = ('code',)
    actions = ['deactivate_expired_codes']

    def deactivate_expired_codes(self, request, queryset):
        expired_codes = queryset.filter(end_date__lt=now())
        count = expired_codes.count()
        expired_codes.delete()
        self.message_user(request, f"{count} کد تخفیف منقضی حذف شد.")
    deactivate_expired_codes.short_description = _('حذف کدهای تخفیف منقضی‌شده')

admin.site.register(DiscountCode, DiscountCodeAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'customer', 'address', 'total_amount', 'discount_code')
    list_filter = ('status', 'customer')
    search_fields = ('id', 'customer__name')
    actions = ['mark_as_completed']

    def mark_as_completed(self, request, queryset):
        count = queryset.update(status='completed')
        self.message_user(request, f"{count} سفارش به وضعیت 'تکمیل شده' تغییر یافت.")
    mark_as_completed.short_description = _('تغییر وضعیت به تکمیل‌شده')

admin.site.register(Order, OrderAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total_price', 'created_at')
    search_fields = ('customer__name',)
    list_filter = ('created_at',)

admin.site.register(Cart, CartAdmin)

from .models import CartItem

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'cart')
    search_fields = ('product__name', 'cart__customer__name')
    list_filter = ('product',)

admin.site.register(CartItem, CartItemAdmin)

from .models import OrderItem

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'discount_amount')
    list_filter = ('order', 'product')
    search_fields = ('product__name', 'order__id')

admin.site.register(OrderItem, OrderItemAdmin)
