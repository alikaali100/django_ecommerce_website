from django.db import models
from core.models import BaseModel
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.timezone import now, timedelta
class Customer(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message="Phone number must start with '09' and be 11 digits long."
            )
        ]
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    otp = models.CharField(max_length=6, blank=True, null=True)  # Add OTP field
    otp_expiry = models.DateTimeField(blank=True, null=True)  # Add OTP expiry field

    def generate_otp(self):
        """Generate a 6-digit OTP and set an expiry time."""
        import random
        self.otp = str(random.randint(100000, 999999))
        self.otp_expiry = now() + timedelta(minutes=10)  # OTP valid for 5 minutes
        self.save()
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Address(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    detailed_address = models.TextField(max_length=100)

    def __str__(self):
        return f"{self.province}, {self.city}"
