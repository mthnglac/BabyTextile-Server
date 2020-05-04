from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import SupplierBillingAddress


@receiver(pre_save, sender=SupplierBillingAddress)
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
