# Generated by Django 3.0.5 on 2020-05-06 22:51

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_unique_id', models.CharField(blank=True, max_length=120, verbose_name='Unique Cart ID')),
                ('qty', models.PositiveSmallIntegerField(default=0, verbose_name='Quantity')),
                ('subtotal', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=100, verbose_name='Subtotal')),
                ('total', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=100, verbose_name='Total')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of Cart')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of Cart')),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_item_id', models.CharField(blank=True, max_length=120, verbose_name='Unique Item ID')),
                ('qty', models.PositiveSmallIntegerField(default=1, verbose_name='Quantity')),
                ('line_total', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=100, verbose_name='Line Total')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of Cart')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of Cart')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts.Cart', verbose_name='Cart')),
            ],
            options={
                'verbose_name': 'Cart Item',
                'verbose_name_plural': 'Cart Items',
                'ordering': ['-updated_at'],
            },
        ),
    ]
