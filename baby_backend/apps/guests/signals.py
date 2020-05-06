from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from baby_backend.utils.utils import unique_vendor_guest_id_generator

from ..carts.models import Cart
from .models import GuestVendor


@receiver(pre_save, sender=GuestVendor)
def pre_save_guest_vendor(sender, instance, *args, **kwargs):
    guest_vendor_unique_id = unique_vendor_guest_id_generator(instance)
    instance.guest_vendor_unique_id = guest_vendor_unique_id


@receiver(post_save, sender=GuestVendor)
def post_save_guest_vendor_created(sender, instance, created, *args, **kwargs):
    if created and instance.user.username and (not instance.user.is_superuser or not instance.user.is_staff):
        Cart.objects.get_or_create(user=instance.user)
