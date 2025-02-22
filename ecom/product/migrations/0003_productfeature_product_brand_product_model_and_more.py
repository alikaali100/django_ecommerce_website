# Generated by Django 5.1.3 on 2024-12-08 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_category_deleted_at_discount_deleted_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=50)),
                ('display_order', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.TextField(default='DefaultBrand', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='model',
            field=models.TextField(default='DefaultModel', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='discount',
            name='amount',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='discount',
            name='max_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='discount',
            name='type',
            field=models.CharField(choices=[('PG', 'Percentage'), ('FA', 'Fixed Amount')], max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=250),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.PositiveIntegerField(),
        ),
    ]
