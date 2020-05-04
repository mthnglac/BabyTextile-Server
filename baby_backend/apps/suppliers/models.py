from decimal import Decimal

from django.db import models
from django.utils.translation import ugettext_lazy as _

BILLING_TYPE = (
    ('individual', _('Individual')),
    ('corporate', _('Corporate'))
)


class Supplier(models.Model):
    company_name = models.CharField(max_length=25, unique=True, blank=False, verbose_name=_('Company Name'))
    tax_number = models.BigIntegerField(blank=False, unique=True, verbose_name=_('Tax Number'))
    tax_office = models.CharField(max_length=100, blank=True, verbose_name=_('Tax Office'))
    phone_number = models.CharField(max_length=17, null=True, unique=True, blank=True, verbose_name=_('Phone Number'))
    total_purchase_amount = models.DecimalField(
        blank=True, default=Decimal(0.00), max_digits=100, decimal_places=2, verbose_name=_('Total Purchase Amount'))
    paid_amount = models.DecimalField(
        blank=True, default=Decimal(0.00), max_digits=100, decimal_places=2, verbose_name=_('Paid Amount'))
    unpaid_amount = models.DecimalField(
        blank=True, default=Decimal(0.00), max_digits=100, decimal_places=2, verbose_name=_('Unpaid Amount'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Supplier'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Supplier'))

    def __str__(self):
        return self.company_name

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Supplier')
        verbose_name_plural = _('Suppliers')

    def save(self, *args, **kwargs):
        # self.unpaid_amount = (self.total_purchase_amount - self.paid_amount)
        super(Supplier, self).save(*args, **kwargs)


class SupplierDeliveryAddress(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name=_('Supplier'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active/Passive'))
    title = models.CharField(max_length=30, blank=False, verbose_name=_('Title'))
    address = models.TextField(blank=False, verbose_name=_('Address Line'))
    zip_code = models.IntegerField(blank=True, null=True, verbose_name=_('ZIP / Postal Code'))
    district = models.CharField(max_length=30, blank=False, verbose_name=_('District'))
    city = models.CharField(max_length=30, blank=False, verbose_name=_('City'))
    country = models.CharField(max_length=30, blank=True, default='Turkey', verbose_name=_('Country'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Address'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Address'))

    def __str__(self):
        return '{} | {} {} {}'.format(self.supplier, self.address, self.district, self.city)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Supplier Delivery Address')
        verbose_name_plural = _('Supplier Delivery Addresses')


class SupplierBillingAddress(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name=_('Supplier'))
    title = models.CharField(max_length=30, blank=False, verbose_name=_('Title'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active/Passive'))
    address = models.TextField(blank=False, verbose_name=_('Address Line'))
    zip_code = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=_('ZIP / Postal Code'))
    district = models.CharField(max_length=30, blank=False, verbose_name=_('District'))
    city = models.CharField(max_length=30, blank=False, verbose_name=_('City'))
    country = models.CharField(max_length=30, blank=True, default='Turkey', verbose_name=_('Country'))
    billing_type = models.CharField(blank=True, default='individual', max_length=50, choices=BILLING_TYPE,
                                    verbose_name=_('Billing Type'))
    company_name = models.CharField(blank=True, max_length=100, verbose_name=_('Company Name'))
    tax_number = models.BigIntegerField(blank=True, default=0, verbose_name=_('Tax Number'))
    tax_office = models.CharField(max_length=100, blank=True, verbose_name=_('Tax Office'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Billing Address'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Billing Address'))

    def __str__(self):
        return '{} | {} {} {}'.format(self.supplier, self.address, self.district, self.city)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Supplier Billing Address')
        verbose_name_plural = _('Supplier Billing Addresses')
