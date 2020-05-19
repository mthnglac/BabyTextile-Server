# Generated by Django 3.0.5 on 2020-05-19 22:19

import baby_backend.apps.customers.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_unique_id', models.CharField(blank=True, max_length=120, verbose_name='Customer ID')),
                ('tc_number', models.BigIntegerField(verbose_name='Citizenship Number')),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=25, verbose_name='Gender')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Birth Date')),
                ('phone_number', models.CharField(max_length=17, verbose_name='Phone Number')),
                ('sms_request', models.BooleanField(default=False, verbose_name='SMS Request')),
                ('email_request', models.BooleanField(default=False, verbose_name='Email Request')),
                ('image', models.ImageField(blank=True, null=True, upload_to=baby_backend.apps.customers.models.upload_customer_image_loc, verbose_name='Image')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='Slug')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of Customer')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of Customer')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='CustomerDiscount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('code', models.CharField(blank=True, max_length=120, null=True, unique=True, verbose_name='Code')),
                ('discount', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='Discount')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active/Passive')),
                ('valid_from', models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='Valid From')),
                ('valid_until', models.DateField(verbose_name='Valid Until')),
                ('num_uses', models.PositiveSmallIntegerField(default=0, verbose_name='Number of times already used')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of Discount Code')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of Discount Code')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.Customer', verbose_name='Customer')),
            ],
            options={
                'verbose_name': 'Customer Discount',
                'verbose_name_plural': 'Customer Discounts',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='CustomerDeliveryAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='Title')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active/Passive')),
                ('address', models.TextField(verbose_name='Address Line')),
                ('zip_code', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='ZIP / Postal Code')),
                ('district', models.CharField(max_length=30, verbose_name='District')),
                ('city', models.CharField(max_length=30, verbose_name='City')),
                ('country', models.CharField(blank=True, default='Turkey', max_length=30, verbose_name='Country')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of Address')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of Address')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.Customer', verbose_name='Customer')),
            ],
            options={
                'verbose_name': 'Customer Delivery Address',
                'verbose_name_plural': 'Customer Delivery Addresses',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='CustomerBillingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='Title')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active/Passive')),
                ('address', models.TextField(verbose_name='Address Line')),
                ('zip_code', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='ZIP / Postal Code')),
                ('district', models.CharField(max_length=30, verbose_name='District')),
                ('city', models.CharField(max_length=30, verbose_name='City')),
                ('country', models.CharField(blank=True, default='Turkey', max_length=30, verbose_name='Country')),
                ('billing_type', models.CharField(blank=True, choices=[('individual', 'Individual'), ('corporate', 'Corporate')], default='individual', max_length=50, verbose_name='Billing Type')),
                ('company_name', models.CharField(blank=True, max_length=100, verbose_name='Company Name')),
                ('tax_number', models.BigIntegerField(blank=True, default=0, verbose_name='Tax Number')),
                ('tax_office', models.CharField(blank=True, max_length=100, verbose_name='Tax Office')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of Billing Address')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of Billing Address')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.Customer', verbose_name='Customer')),
            ],
            options={
                'verbose_name': 'Customer Billing Address',
                'verbose_name_plural': 'Customer Billing Addresses',
                'ordering': ['-updated_at'],
            },
        ),
    ]
