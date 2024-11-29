from django.test import TestCase
from orders.models import Order, OrderItem
from customers.models import Customer, Address
from product.models import Product, Category

class OrderModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com"
        )
        self.address = Address.objects.create(
            customer=self.customer,
            province="California",
            city="San Francisco",
            detailed_address="123 Market St"
        )
        self.category = Category.objects.create(name="Books")
        self.product = Product.objects.create(
            name="Django for Beginners",
            price=39.99,
            stock=10,
            category=self.category
        )

    def test_create_order(self):
        order = Order.objects.create(
            customer=self.customer,
            address=self.address,
            total_amount=39.99,
            status="Pending"
        )
        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
            price=39.99,
            discount_amount=0
        )
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().product, self.product)
