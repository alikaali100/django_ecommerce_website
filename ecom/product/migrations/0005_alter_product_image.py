# Generated by Django 5.1.3 on 2024-12-18 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_productfeature_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.URLField(blank=True, default=1, max_length=500),
            preserve_default=False,
        ),
    ]
