from django.test import TestCase
from customers.models import Customer

class CustomerModelTest(TestCase):
    def test_create_customer(self):
        customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone_number="1234567890"
        )
        self.assertEqual(customer.first_name, "John")
        self.assertEqual(customer.last_name, "Doe")
        self.assertEqual(customer.email, "john.doe@example.com")
        self.assertFalse(customer.is_deleted)

    def test_soft_delete_customer(self):
        customer = Customer.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com",
            phone_number="0987654321"
        )
        customer.is_deleted = True
        customer.save()
        self.assertTrue(customer.is_deleted)
