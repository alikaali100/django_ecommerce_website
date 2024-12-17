from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from product.models import Product, Category, Discount, ProductFeature
from customers.models import Customer, Address
from orders.models import Order, DiscountCode


class Command(BaseCommand):
    help = 'Set up user groups and permissions'

    def handle(self, *args, **kwargs):
        try:
            # Create groups
            product_manager_group, _ = Group.objects.get_or_create(name='Product Manager')
            supervisor_group, _ = Group.objects.get_or_create(name='Supervisor')
            operator_group, _ = Group.objects.get_or_create(name='Operator')

            # Define content types
            product_ct = ContentType.objects.get_for_model(Product)
            product_feature_ct = ContentType.objects.get_for_model(ProductFeature)
            category_ct = ContentType.objects.get_for_model(Category)
            discount_ct = ContentType.objects.get_for_model(Discount)
            discount_code_ct = ContentType.objects.get_for_model(DiscountCode)
            customer_ct = ContentType.objects.get_for_model(Customer)
            address_ct = ContentType.objects.get_for_model(Address)
            order_ct = ContentType.objects.get_for_model(Order)

            # Assign permissions to Product Manager
            product_manager_permissions = Permission.objects.filter(
                content_type__in=[product_ct, product_feature_ct, category_ct, discount_ct, discount_code_ct],
                codename__in=[
                    'add_product', 'change_product', 'delete_product', 'view_product',
                    'add_category', 'change_category', 'delete_category', 'view_category',
                    'add_discount', 'change_discount', 'delete_discount', 'view_discount',
                    'add_productfeature', 'change_productfeature', 'delete_productfeature', 'view_productfeature',
                    'add_discountcode', 'change_discountcode', 'delete_discountcode', 'view_discountcode',
                ]
            )
            product_manager_group.permissions.set(product_manager_permissions)

            # Assign read-only permissions to Supervisor
            supervisor_permissions = Permission.objects.filter(
                content_type__in=[product_ct, product_feature_ct, category_ct, discount_ct, discount_code_ct, customer_ct, address_ct, order_ct],
                codename__in=[
                    'view_product', 'view_productfeature', 'view_category', 'view_discountcode', 'view_discount', 'view_customer', 'view_address', 'view_order'
                ]
            )
            supervisor_group.permissions.clear()
            supervisor_group.permissions.add(*supervisor_permissions)

            # Assign permissions to Operator
            operator_permissions = Permission.objects.filter(
                content_type__in=[customer_ct, address_ct, order_ct],
                codename__in=[
                    'add_customer', 'change_customer', 'delete_customer', 'view_customer',
                    'add_address', 'change_address', 'delete_address', 'view_address',
                    'add_order', 'change_order', 'delete_order', 'view_order',
                ]
            )
            operator_group.permissions.set(operator_permissions)

            self.stdout.write(self.style.SUCCESS('Successfully set up groups and permissions'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error setting up permissions: {e}"))
