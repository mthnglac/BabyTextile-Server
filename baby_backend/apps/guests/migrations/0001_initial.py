# Generated by Django 3.0.5 on 2020-06-01 22:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GuestVendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_vendor_unique_id', models.CharField(blank=True, max_length=120, verbose_name='Unique Guest Vendor ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active/Passive')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of Balance')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of Balance')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Guest Vendor',
                'verbose_name_plural': 'Guest Vendors',
                'ordering': ['-updated_at'],
            },
        ),
    ]
