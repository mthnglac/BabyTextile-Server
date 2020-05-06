# Generated by Django 3.0.5 on 2020-05-06 22:51

import baby_backend.apps.products.models
from decimal import Decimal
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('suppliers', '0001_initial'),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_unique_id', models.CharField(blank=True, max_length=120, null=True, unique=True, verbose_name='Product ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Name')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('featured', models.BooleanField(default=False, verbose_name='Featured')),
                ('best_seller', models.BooleanField(default=False, verbose_name='Best Seller')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='Slug')),
                ('sku', models.CharField(blank=True, max_length=50, verbose_name='Stock Keeping Unit')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=25, verbose_name='Purchase Price')),
                ('old_purchase_price', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=25, verbose_name='Old Purchase Price')),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=25, verbose_name='Sale Price')),
                ('old_sale_price', models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=25, verbose_name='Old Sale Price')),
                ('sold_qty', models.PositiveIntegerField(blank=True, default=0, verbose_name='Sold Quantity')),
                ('purchased_stock', models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Purchased Stock')),
                ('available_stock', models.IntegerField(blank=True, default=0, verbose_name='Available Stock')),
                ('meta_keywords', models.CharField(blank=True, help_text='Comma-delimited set of SEO keywords for meta tag', max_length=255, verbose_name='META Keywords')),
                ('meta_description', models.CharField(blank=True, help_text='Content for description meta tag', max_length=255, verbose_name='META Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of Product')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of Product')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductBrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Brand')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of Product Brand')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of Product Brand')),
            ],
            options={
                'verbose_name': 'Product Brand',
                'verbose_name_plural': 'Product Brands',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='Category')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('active', models.BooleanField(default=True)),
                ('meta_keywords', models.CharField(blank=True, help_text='Comma-delimited set of SEO keywords for meta tag', max_length=255, verbose_name='META Keywords')),
                ('meta_description', models.CharField(blank=True, help_text='Content for description meta tag', max_length=255, verbose_name='META Description')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of Category')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of Category')),
            ],
            options={
                'verbose_name': 'Product Category',
                'verbose_name_plural': 'Product Categories',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, unique=True, verbose_name='Color')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of Color')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of Color')),
            ],
            options={
                'verbose_name': 'Product Color',
                'verbose_name_plural': 'Product Colors',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_month', models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Start Month')),
                ('end_month', models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='End Month')),
                ('age', models.CharField(blank=True, max_length=10, verbose_name='Age')),
                ('size', models.PositiveSmallIntegerField(unique=True, verbose_name='Size')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of Size')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of Size')),
            ],
            options={
                'verbose_name': 'Product Size',
                'verbose_name_plural': 'Product Sizes',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductVAT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vat_rate', models.DecimalField(decimal_places=2, max_digits=10, unique=True, verbose_name='VAT Rate')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of Product VAT')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of Product VAT')),
            ],
            options={
                'verbose_name': 'Product VAT',
                'verbose_name_plural': 'Product VATs',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Model')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of Product Model')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of Product Model')),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.ProductBrand', verbose_name='Brand Information')),
            ],
            options={
                'verbose_name': 'Product Model',
                'verbose_name_plural': 'Product Models',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Name')),
                ('image', models.ImageField(null=True, upload_to=baby_backend.apps.products.models.upload_product_image_loc, verbose_name='Image')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of File')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of File')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Product Image',
                'verbose_name_plural': 'Product Images',
                'ordering': ['updated_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Name')),
                ('file', models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/app/baby_backend/protected_media'), upload_to=baby_backend.apps.products.models.upload_product_file_loc, verbose_name='File')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of File')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of File')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Product File',
                'verbose_name_plural': 'Product Files',
                'ordering': ['updated_at'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='brand_information',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.ProductBrand', verbose_name='Brand Information'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(to='products.ProductCategory', verbose_name='Category'),
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.ProductColor', verbose_name='Color'),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(to='products.ProductSize', verbose_name='Size'),
        ),
        migrations.AddField(
            model_name='product',
            name='supplier',
            field=models.ManyToManyField(to='suppliers.Supplier', verbose_name='Supplier'),
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='product',
            name='vat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.ProductVAT', verbose_name='VAT'),
        ),
    ]
