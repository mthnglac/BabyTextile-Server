from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from .models import Order
from baby_backend.utils.utils import unique_order_id_generator


@receiver(pre_save, sender=Order)
def pre_save_create_order_id(sender, instance, *args, **kwargs):
    # if instance has a order other than currently using, disable them.
    # bu satiri su olasilik yuzunden kaldiriyorum: ya arka arkaya 2 siparis girerse??
    # qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    # if qs.exists():
    #     qs.update(active=False)

    # creating order_id
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


@receiver(post_delete, sender=Order)
def post_delete_order(sender, instance, *args, **kwargs):
    # if order has deleted, delete related shipping_information
    if instance.shipping_information is not None:
        instance.shipping_information.delete()
