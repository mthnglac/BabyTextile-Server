# Generated by Django 3.0.5 on 2020-06-01 23:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_remove_product_variant'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariant',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.ProductImage', verbose_name='Image'),
        ),
    ]
