# Generated by Django 5.1.5 on 2025-01-21 15:14

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_remove_customer_otp_remove_customer_otp_expiry'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name': 'آدرس', 'verbose_name_plural': 'آدرس\u200cها'},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': 'مشتری', 'verbose_name_plural': 'مشتریان'},
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=100, verbose_name='شهر'),
        ),
        migrations.AlterField(
            model_name='address',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL, verbose_name='مشتری'),
        ),
        migrations.AlterField(
            model_name='address',
            name='detailed_address',
            field=models.TextField(max_length=100, verbose_name='آدرس دقیق'),
        ),
        migrations.AlterField(
            model_name='address',
            name='province',
            field=models.CharField(max_length=100, verbose_name='استان'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='ایمیل'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(max_length=50, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name',
            field=models.CharField(max_length=50, verbose_name='نام خانوادگی'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message="شماره تلفن باید با '09' شروع شود و 11 رقم باشد.", regex='^09\\d{9}$')], verbose_name='شماره تلفن'),
        ),
    ]
