from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from baby_backend.utils.utils import (
    unique_vendor_discount_code_generator,
    unique_vendor_id_generator,
)

from ..billing.models import BillingProfile
from ..carts.models import Cart
from .models import Vendor, VendorBalance, VendorBillingAddress, VendorDiscount


@receiver(pre_save, sender=Vendor)
def pre_save_create_vendor(sender, instance, *args, **kwargs):
    if not instance.vendor_id:
        vendor_id = unique_vendor_id_generator(instance)
        instance.vendor_id = vendor_id


@receiver(post_save, sender=Vendor)
def post_save_vendor_created(sender, instance, created, *args, **kwargs):
    if created:
        if instance.user.username and (not instance.user.is_superuser or not instance.user.is_staff):
            BillingProfile.objects.get_or_create(user=instance.user)
            Cart.objects.get_or_create(user=instance.user)
            VendorBalance.objects.get_or_create(vendor=instance)


@receiver(pre_save, sender=VendorBillingAddress)
def pre_save_billing_address(sender, instance, *args, **kwargs):
    # if not billing_type entered ?? re-clear all company data even if entered!!
    if not hasattr(instance, 'billing_type'):
        instance.company_name = ''
        instance.tax_number = 0
        instance.tax_office = ''
    # in serializer, all validations working for billing_type but still as a plan B, I add a validation here.
    # if billing_type entered as corporate but no company infos ?? clear them all!
    elif hasattr(instance, 'billing_type') and instance.billing_type == 'corporate':
        if instance.company_name == '' or instance.tax_number == 0 or instance.tax_office == '':
            instance.billing_type = 'individual'
            instance.company_name = ''
            instance.tax_number = 0
            instance.tax_office = ''
    # just fresh start
    elif hasattr(instance, 'billing_type') and instance.billing_type == 'individual':
        instance.company_name = ''
        instance.tax_number = 0
        instance.tax_office = ''


@receiver(pre_save, sender=VendorDiscount)
def pre_save_create_vendor_discount_code(sender, instance, *args, **kwargs):
    if not instance.code:
        code = unique_vendor_discount_code_generator(instance)
        instance.code = code
