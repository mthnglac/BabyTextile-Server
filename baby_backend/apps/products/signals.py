from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from baby_backend.utils.utils import unique_product_unique_id_generator, unique_slug_generator

from .models import Product


@receiver(pre_save, sender=Product)
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

    if not instance.product_unique_id:
        instance.product_unique_id = unique_product_unique_id_generator(instance)


@receiver(post_save, sender=Product)
def post_save_product(sender, instance, created, *args, **kwargs):
    if not created:
        if instance.cartitem_set:
            for item in instance.cartitem_set.all():
                item.refresh_item()
