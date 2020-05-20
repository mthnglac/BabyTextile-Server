# Generated by Django 3.0.5 on 2020-05-19 22:19

import baby_backend.apps.vendors.models
from decimal import Decimal
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
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_unique_id', models.CharField(blank=True, max_length=120, verbose_name='Unique ID')),
                ('tc_number', models.BigIntegerField(unique=True, verbose_name='Citizenship Number')),
                ('phone_number', models.CharField(max_length=17, unique=True, verbose_name='Phone Number')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Birth Date')),
                ('birth_place', models.CharField(blank=True, max_length=25, verbose_name='Birth Place')),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=25, verbose_name='Gender')),
                ('dealership_agreement', models.BooleanField(default=False, verbose_name='Dealership Agreement')),
                ('sms_request', models.BooleanField(default=False, verbose_name='SMS Request')),
                ('email_request', models.BooleanField(default=False, verbose_name='Email Request')),
                ('commission_rate', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.15'), max_digits=3, verbose_name='Commission Rate')),
                ('total_sales_qty', models.PositiveIntegerField(blank=True, default=0, verbose_name='Total Sales Quantity')),
                ('total_sales_amount', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=100, verbose_name='Total Sales Amount')),
                ('image', models.ImageField(blank=True, null=True, upload_to=baby_backend.apps.vendors.models.upload_vendor_image_loc, verbose_name='Image')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='Slug')),
                ('sales_quota', models.PositiveSmallIntegerField(blank=True, default=100, verbose_name='Sales Quota')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of Vendor')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of Vendor')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Vendor',
                'verbose_name_plural': 'Vendors',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='VendorDiscount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('code', models.CharField(blank=True, max_length=120, null=True, unique=True, verbose_name='Code')),
                ('discount', models.DecimalField(decimal_places=2, max_digits=3, verbose_name='Discount')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active/Passive')),
                ('valid_from', models.DateField(default=django.utils.timezone.now, verbose_name='Valid From')),
                ('valid_until', models.DateField(verbose_name='Valid Until')),
                ('num_uses', models.PositiveSmallIntegerField(default=0, verbose_name='Number of times already used')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of Discount Code')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of Discount Code')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendors.Vendor', verbose_name='Vendor')),
            ],
            options={
                'verbose_name': 'Vendor Discount',
                'verbose_name_plural': 'Vendor Discounts',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='VendorDeliveryAddress',
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
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendors.Vendor', verbose_name='Vendor')),
            ],
            options={
                'verbose_name': 'Vendor Delivery Address',
                'verbose_name_plural': 'Vendor Delivery Address',
            },
        ),
        migrations.CreateModel(
            name='VendorCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('phone_number', models.CharField(max_length=17, verbose_name='Phone Number')),
                ('city', models.CharField(max_length=30, verbose_name='City')),
                ('district', models.CharField(max_length=30, verbose_name='District')),
                ('zip_code', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='ZIP / Postal Code (Optional)')),
                ('address', models.TextField(verbose_name='Address Line')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of Vendor')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of Vendor')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendors.Vendor', verbose_name='Vendor Customer')),
            ],
            options={
                'verbose_name': 'Vendor Customer',
                'verbose_name_plural': 'Vendor Customers',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='VendorBillingAddress',
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
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of Address')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of Address')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendors.Vendor', verbose_name='Vendor')),
            ],
            options={
                'verbose_name': 'Vendor Billing Address',
                'verbose_name_plural': 'Vendor Billing Address',
            },
        ),
        migrations.CreateModel(
            name='VendorBankAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_holder_first_name', models.CharField(blank=True, max_length=20, verbose_name='Account Holder First Name')),
                ('account_holder_last_name', models.CharField(blank=True, max_length=20, verbose_name='Account Holder Last Name')),
                ('iban', models.CharField(blank=True, max_length=26, null=True, unique=True, verbose_name='IBAN')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of Bank Account')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of Bank Account')),
                ('vendor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='vendors.Vendor', verbose_name='Vendor')),
            ],
            options={
                'verbose_name': 'Vendor Bank Account',
                'verbose_name_plural': 'Vendor Bank Accounts',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='VendorBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtotal_balance', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=25, verbose_name='Subtotal Balance')),
                ('withholding_tax_deduction', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=25, verbose_name='Withholding Tax Deduction')),
                ('total_balance', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=25, verbose_name='Total Balance')),
                ('paid_balance', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=25, verbose_name='Paid Balance')),
                ('money_demand', models.BooleanField(blank=True, default=False, verbose_name='Money Demand')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of Balance')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of Balance')),
                ('vendor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='vendors.Vendor', verbose_name='Vendor')),
            ],
            options={
                'verbose_name': 'Vendor Balance',
                'verbose_name_plural': 'Vendor Balances',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='VendorInstagram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=25, verbose_name='Username')),
                ('old_username', models.CharField(blank=True, max_length=25, verbose_name='Old Username')),
                ('followers_qty', models.PositiveIntegerField(blank=True, default=0, verbose_name='Count of Followers')),
                ('old_followers_qty', models.PositiveIntegerField(blank=True, default=0, verbose_name='Count of Old Followers')),
                ('follower_increase_rate', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=20, verbose_name='Follower Increase Rate')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of Instagram')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of Instagram')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendors.Vendor', verbose_name='Vendor')),
            ],
            options={
                'verbose_name': 'Vendor Instagram',
                'verbose_name_plural': 'Vendor Instagrams',
                'ordering': ['-updated_at'],
                'unique_together': {('vendor', 'username')},
            },
        ),
    ]