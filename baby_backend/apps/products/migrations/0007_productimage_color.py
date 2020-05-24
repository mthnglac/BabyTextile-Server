# Generated by Django 3.0.5 on 2020-05-23 23:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20200520_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.ProductColor', verbose_name='Product Color'),
        ),
    ]
