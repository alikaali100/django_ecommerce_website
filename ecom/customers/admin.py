from django.contrib import admin
from .models import Customer, Address
from django.utils.translation import gettext_lazy as _

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'is_active')
    list_filter = ('is_active', 'date_joined')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'password')
        }),
        (_('اطلاعات پیشرفته'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )

class AddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'province', 'city', 'detailed_address')
    list_filter = ('province', 'city')
    search_fields = ('province', 'city', 'detailed_address', 'customer__first_name', 'customer__last_name')
    ordering = ('-created_at',)

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Address, AddressAdmin)
