from django.test import TestCase
from django.utils.timezone import now, timedelta
from core.models import BaseModel
from product.models import Product
from customers.models import Customer, Address
from orders.models import DiscountCode, Order, OrderItem

class DiscountCodeModelTest(TestCase):
    def setUp(self):
        self.discount_code = DiscountCode.objects.create(
            code="SUMMER2024",
            type="PG",
            amount=10,
            max_amount=50,
            start_date=now(),
            end_date=now() + timedelta(days=30),
            usage_limit=100,
        )

    def test_discount_code_creation(self):
        self.assertEqual(self.discount_code.code, "SUMMER2024")
        self.assertEqual(self.discount_code.type, "PG")
        self.assertEqual(self.discount_code.amount, 10)
        self.assertEqual(self.discount_code.max_amount, 50)
        self.assertEqual(self.discount_code.usage_limit, 100)

class OrderModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(first_name="John",last_name="Doe",email="ali@gmail.com")
        self.address = Address.objects.create(customer=self.customer, province="Main St", city="Cityville", detailed_address="State")
        self.discount_code = DiscountCode.objects.create(
            code="SUMMER2024",
            type="PG",
            amount=10,
            max_amount=50,
            start_date=now(),
            end_date=now() + timedelta(days=30),
            usage_limit=100,
        )
        self.order = Order.objects.create(
            customer=self.customer,
            address=self.address,
            discount_code=self.discount_code,
            total_amount=500,
        )

    def test_order_creation(self):
        self.assertEqual(self.order.customer, self.customer)
        self.assertEqual(self.order.address, self.address)
        self.assertEqual(self.order.discount_code, self.discount_code)
        self.assertEqual(self.order.total_amount, 500)
        self.assertEqual(self.order.status, Order.PENDING)

    def test_order_str(self):
        self.assertEqual(str(self.order), f"Order {self.order.id} - Pending")

class OrderItemModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(first_name="John",last_name="Doe",email="ali1@gmail.com")
        self.address = Address.objects.create(customer=self.customer, province="Main St", city="Cityville", detailed_address="State")
        self.product = Product.objects.create(name="Test Product", price=100,stock=20)
        self.order = Order.objects.create(
            customer=self.customer,
            address=self.address,
            total_amount=500,
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=200,
            discount_amount=20,
        )

    def test_order_item_creation(self):
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.price, 200)
        self.assertEqual(self.order_item.discount_amount, 20)

    def test_order_item_str(self):
        self.assertEqual(str(self.order_item), f"2 x {self.product.name} (Order #{self.order.id})")
