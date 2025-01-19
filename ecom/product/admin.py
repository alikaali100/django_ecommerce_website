from django.contrib import admin
from .models import Product, Category, ProductFeature, Discount
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'brand', 'model', 'category', 'discounted_price_column')
    search_fields = ('name', 'brand', 'model', 'category__name')
    list_filter = ('brand', 'category', 'price', 'stock')
    list_editable = ('price', 'stock')
    fields = ('name', 'description', 'price', 'stock', 'brand', 'model', 'category', 'image', 'discounts')
    
    def discounted_price_column(self, obj):
        return obj.discounted_price
    discounted_price_column.short_description = 'قیمت با تخفیف' 
    
    # تعریف اکشن‌ها
    actions = ['adjust_price']
    def adjust_price(self, request, queryset):
        """
        اکشنی برای افزایش یا کاهش قیمت محصولات
        """
        percentage = 5  # درصد تغییر قیمت
        for product in queryset:
            product.price += product.price * (percentage / 100)  # افزایش قیمت
            product.save()
        self.message_user(request, f"قیمت {queryset.count()} محصول به‌روزرسانی شد.")

    adjust_price.short_description = 'افزایش ۵٪ قیمت محصولات انتخاب‌شده'
admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_count')
    search_fields = ('name',)

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = _('تعداد محصولات')

admin.site.register(Category, CategoryAdmin)

class ProductFeatureAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'product', 'display_order')
    search_fields = ('key', 'value', 'product__name')
    list_filter = ('product',)

admin.site.register(ProductFeature, ProductFeatureAdmin)

class DiscountAdmin(admin.ModelAdmin):
    list_display = ('type', 'amount', 'max_amount', 'start_date', 'end_date', 'product_count')
    list_filter = ('type', 'start_date', 'end_date')
    search_fields = ('type',)
    actions = ['close_expired_discounts']

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = _('تعداد محصولات مرتبط')

    def close_expired_discounts(self, request, queryset):
        expired_discounts = queryset.filter(end_date__lt=now())
        count = expired_discounts.count()
        expired_discounts.delete()
        self.message_user(request, f"{count} تخفیف منقضی حذف شد.")
    close_expired_discounts.short_description = _('حذف تخفیف‌های منقضی‌شده')

admin.site.register(Discount, DiscountAdmin)
