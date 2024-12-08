from django.db import models
from core.models import BaseModel
from django.core.validators import RegexValidator

class Customer(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11,  
            validators=[
            RegexValidator(regex=r'^09\d{9}$')])

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Address(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    detailed_address = models.TextField(max_length=100)

    def __str__(self):
        return f"{self.province}, {self.city}"
