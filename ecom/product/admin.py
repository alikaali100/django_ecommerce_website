from django.contrib import admin
from .models import Product,Category,ProductFeature,Discount

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductFeature)
admin.site.register(Discount)
