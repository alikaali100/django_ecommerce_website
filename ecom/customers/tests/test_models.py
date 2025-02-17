from django.test import TestCase
from customers.models import Customer, Address
from django.core.exceptions import ValidationError
from django.utils.timezone import now

class CustomerModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="09123456789"
        )

    def test_customer_creation(self):
        self.assertEqual(self.customer.first_name, "John")
        self.assertEqual(self.customer.last_name, "Doe")
        self.assertEqual(self.customer.email, "john.doe@example.com")
        self.assertEqual(self.customer.phone_number, "09123456789")

    def test_customer_str_representation(self):
        self.assertEqual(str(self.customer), "John Doe")

    def test_invalid_phone_number(self):
        with self.assertRaises(ValidationError):
            invalid_customer = Customer(
                first_name="Invalid",
                last_name="Phone",
                email="invalid.phone@example.com",
                phone_number="1234567890"  # Invalid phone number
            )
            invalid_customer.full_clean()  # Trigger validation manually


class AddressModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com",
            phone_number="09111234567"
        )
        self.address = Address.objects.create(
            customer=self.customer,
            province="Tehran",
            city="Tehran",
            detailed_address="123 Main Street"
        )

    def test_address_creation(self):
        self.assertEqual(self.address.customer, self.customer)
        self.assertEqual(self.address.province, "Tehran")
        self.assertEqual(self.address.city, "Tehran")
        self.assertEqual(self.address.detailed_address, "123 Main Street")

    def test_address_str_representation(self):
        self.assertEqual(str(self.address), "Tehran, Tehran")
