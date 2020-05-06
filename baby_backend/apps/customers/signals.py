from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from baby_backend.utils.utils import (
    unique_customer_discount_code_generator,
    unique_customer_unique_id_generator,
    unique_slug_generator,
)

from ..billing.models import BillingProfile
from ..carts.models import Cart
from .models import Customer, CustomerBillingAddress, CustomerDiscount


@receiver(pre_save, sender=Customer)
def pre_save_create_user(sender, instance, *args, **kwargs):
    if not instance.customer_unique_id:
        instance.customer_unique_id = unique_customer_unique_id_generator(instance)

    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver(post_save, sender=Customer)
def post_save_customer_created(sender, instance, created, *args, **kwargs):
    if created \
            and instance.user.username \
            and (not instance.user.is_superuser or not instance.user.is_staff):
        BillingProfile.objects.get_or_create(user=instance.user)
        Cart.objects.get_or_create(user=instance.user)


@receiver(pre_save, sender=CustomerBillingAddress)
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


@receiver(pre_save, sender=CustomerDiscount)
def pre_save_customer_discount(sender, instance, *args, **kwargs):
    if not instance.code:
        code = unique_customer_discount_code_generator(instance)
        instance.code = code
