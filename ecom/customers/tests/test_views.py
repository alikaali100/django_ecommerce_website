from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from customers.models import Customer
from django.core import mail
from django.utils.timezone import now
from datetime import timedelta

class RegisterTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')  # URL for the register endpoint

        # Valid customer data for registration
        self.valid_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "Test@1234"
        }

        # Invalid customer data
        self.invalid_data = {
            "username": "",
            "email": "notanemail",
            "password": "123"
        }

    def test_register_success(self):
        """Test successful registration with valid data"""
        response = self.client.post(self.register_url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Registration successful.")
        self.assertTrue(Customer.objects.filter(email=self.valid_data['email']).exists())

    def test_register_invalid_email(self):
        """Test registration fails with invalid email format"""
        response = self.client.post(self.register_url, {
            "username": "user",
            "email": "invalidemail",
            "password": "Valid@1234"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_register_missing_fields(self):
        """Test registration fails when required fields are missing"""
        response = self.client.post(self.register_url, {
            "username": "",
            "email": "",
            "password": ""
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)

from django.contrib.auth.hashers import make_password

class LoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')

        # Create a test user
        self.customer = Customer.objects.create(
            username="testuser",
            email="testuser@example.com",
            password=make_password("Test@1234")  # Hash the password
        )

    def test_login_success(self):
        """Test successful login with correct credentials"""
        response = self.client.post(self.login_url, {
            "email": "testuser@example.com",
            "password": "Test@1234"
        })
        print(response.data)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_email(self):
        """Test login fails with invalid email"""
        response = self.client.post(self.login_url, {
            "email": "invaliduser@example.com",
            "password": "Test@1234"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Invalid credentials.")

    def test_login_invalid_password(self):
        """Test login fails with incorrect password"""
        response = self.client.post(self.login_url, {
            "email": "testuser@example.com",
            "password": "WrongPassword"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Invalid credentials.")

    def test_login_missing_fields(self):
        """Test login fails when email or password is missing"""
        response = self.client.post(self.login_url, {
            "email": "",
            "password": ""
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Email and password are required.")


class OTPSendTestCase(APITestCase):
    def setUp(self):
        # URL for sending OTP
        self.send_otp_url = reverse('send_otp') 
        
        # Create a customer for testing
        self.customer = Customer.objects.create(
            username="testuser",
            email="testuser@example.com",
            password="Test@1234",
        )
    
    def test_send_otp_success(self):
        """Test that OTP is sent successfully to the provided email"""
        response = self.client.post(self.send_otp_url, {"email": "testuser@example.com"})
        
        # Check if the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)  # Check for the 'message' key in the response
        self.assertEqual(response.data["message"], "OTP sent successfully.")
        
        # Verify that an email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Your OTP Code", mail.outbox[0].subject)


        
    def test_send_otp_invalid_email(self):
        """Test that sending OTP fails when email is not registered"""
        response = self.client.post(self.send_otp_url, {"email": "invalid@example.com"})
        
        # Check for failure response when email doesn't exist
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)  # Check for the 'error' key in the response
        self.assertEqual(response.data["error"], "Customer with this email not found.")


class OTPValidateTestCase(APITestCase):
    def setUp(self):
        # Create a customer for testing
        self.customer_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'username': 'johndoe',
            'password': 'securepassword123'
        }
        self.customer = Customer.objects.create(**self.customer_data)
        self.customer.set_password('securepassword123')
        self.customer.save()
        self.customer.generate_otp()  # Generate OTP for the user

    def test_validate_otp_success(self):
        """Test that OTP is validated successfully with correct OTP."""
        # Send a valid OTP request
        response = self.client.post('/api/customers/validate-otp/', {
            'email': self.customer.email,
            'otp': self.customer.otp
        })
        # Check that the OTP is successfully validated
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('OTP validated successfully', response.data.get('message'))

    def test_validate_otp_invalid(self):
        """Test that OTP validation fails with an invalid OTP."""
        invalid_otp = '123456'  # An OTP that is not correct
        response = self.client.post('/api/customers/validate-otp/', {
            'email': self.customer.email,
            'otp': invalid_otp
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid or expired OTP', response.data.get('error'))

    def test_validate_otp_expired(self):
        """Test that OTP validation fails after OTP expiry."""
        # Make the OTP expire by setting its expiry to a past time
        self.customer.otp_expiry = now() - timedelta(minutes=10)
        self.customer.save()
        response = self.client.post('/api/customers/validate-otp/', {
            'email': self.customer.email,
            'otp': self.customer.otp
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid or expired OTP', response.data.get('error'))

    def test_validate_otp_non_existing_email(self):
        """Test that OTP validation fails for a non-existing email."""
        non_existing_email = 'nonexistent@example.com'
        response = self.client.post('/api/customers/validate-otp/', {
            'email': non_existing_email,
            'otp': '123456'  # Invalid OTP since the email doesn't exist
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Customer with this email not found', response.data.get('error'))
