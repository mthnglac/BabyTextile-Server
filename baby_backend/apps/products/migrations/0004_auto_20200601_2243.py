# Generated by Django 3.0.5 on 2020-06-01 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20200601_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariant',
            name='title',
            field=models.CharField(blank=True, max_length=20, verbose_name='Title'),
        ),
    ]