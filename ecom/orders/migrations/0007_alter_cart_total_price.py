# Generated by Django 5.1.4 on 2025-01-17 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_cart_total_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
