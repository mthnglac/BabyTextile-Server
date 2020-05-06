# Generated by Django 3.0.5 on 2020-05-06 22:51

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
            name='BillingProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='Active/Passive')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of Billing Profile')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of Billing Profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='billing_profile', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Billing Profile',
                'verbose_name_plural': 'Billing Profiles',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Charge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid', models.BooleanField(default=False, verbose_name='Paid')),
                ('refunded', models.BooleanField(default=False, verbose_name='Refunded')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Create date of Charge')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date of Charge')),
                ('billing_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.BillingProfile', verbose_name='Billing Profile')),
            ],
            options={
                'verbose_name': 'Charge',
                'verbose_name_plural': 'Charges',
                'ordering': ['-updated_at'],
            },
        ),
    ]
