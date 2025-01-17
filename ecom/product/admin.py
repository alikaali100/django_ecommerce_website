from django.contrib import admin
from .models import Product,Category,ProductFeature,Discount
from django.utils.translation import gettext_lazy as _
admin.site.register(Category)
admin.site.register(ProductFeature)
admin.site.register(Discount)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'brand', 'model', 'category', 'discounted_price_column')
    
    search_fields = ('name', 'brand', 'model', 'category__name')
    
    list_filter = ('brand', 'category', 'price', 'stock')
    
    list_editable = ('price', 'stock')
    
    fields = ('name', 'description', 'price', 'stock', 'brand', 'model', 'category', 'image', 'discounts')
    
    def discounted_price_column(self, obj):
        return obj.discounted_price
    discounted_price_column.short_description = 'قیمت با تخفیف'  


admin.site.register(Product, ProductAdmin)
