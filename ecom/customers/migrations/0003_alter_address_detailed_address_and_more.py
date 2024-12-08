# Generated by Django 5.1.3 on 2024-12-08 13:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_address_deleted_at_customer_deleted_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='detailed_address',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(regex='^09\\d{9}$')]),
        ),
    ]
