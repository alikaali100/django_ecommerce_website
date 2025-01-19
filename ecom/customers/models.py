from django.db import models
from core.models import BaseModel
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class Customer(AbstractUser):
    first_name = models.CharField(max_length=50, verbose_name=_('نام'))
    last_name = models.CharField(max_length=50, verbose_name=_('نام خانوادگی'))
    email = models.EmailField(unique=True, verbose_name=_('ایمیل'))
    phone_number = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r'^09\d{9}$',
                message=_("شماره تلفن باید با '09' شروع شود و 11 رقم باشد.")
            )
        ],
        verbose_name=_('شماره تلفن')
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _('مشتری')
        verbose_name_plural = _('مشتریان')

class Address(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses', verbose_name=_('مشتری'))
    province = models.CharField(max_length=100, verbose_name=_('استان'))
    city = models.CharField(max_length=100, verbose_name=_('شهر'))
    detailed_address = models.TextField(max_length=100, verbose_name=_('آدرس دقیق'))

    def __str__(self):
        return f"{self.province}, {self.city}"

    class Meta:
        verbose_name = _('آدرس')
        verbose_name_plural = _('آدرس‌ها')
