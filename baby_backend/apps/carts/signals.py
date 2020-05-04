from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from baby_backend.utils.utils import (
    unique_cart_id_generator,
    unique_cart_item_id_generator,
)

from ..orders.models import Order
from .models import Cart, CartItem


@receiver(pre_save, sender=Cart)
def pre_save_cart(sender, instance, *args, **kwargs):
    if not instance.cart_id:
        instance.cart_id = unique_cart_id_generator(instance)


@receiver(pre_save, sender=CartItem)
def pre_save_cart_item(sender, instance, *args, **kwargs):
    if not instance.item_id:
        instance.item_id = unique_cart_item_id_generator(instance)


@receiver(post_save, sender=CartItem)
def post_save_cart_item_total(sender, instance, created, *args, **kwargs):
    if not created:
        qs = Order.objects.filter(cart__id=instance.cart.id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()
    instance.cart.update_cart()
