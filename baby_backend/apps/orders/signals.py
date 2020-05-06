from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from baby_backend.utils.utils import unique_order_id_generator

from .models import Order


@receiver(pre_save, sender=Order)
def pre_save_create_unique_order_id(sender, instance, *args, **kwargs):
    # if instance has a order other than currently using, disable them.
    # bu satiri su olasilik yuzunden kaldiriyorum: ya arka arkaya 2 siparis girerse??
    # qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    # if qs.exists():
    #     qs.update(active=False)

    # creating order_id
    if not instance.unique_order_id:
        instance.unique_order_id = unique_order_id_generator(instance)


@receiver(post_delete, sender=Order)
def post_delete_order(sender, instance, *args, **kwargs):
    # if order has deleted, delete related shipping_information
    if instance.shipping_information is not None:
        instance.shipping_information.delete()
