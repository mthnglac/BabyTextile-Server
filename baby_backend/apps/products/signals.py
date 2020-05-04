from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from baby_backend.utils.utils import unique_slug_generator, unique_product_id_generator

from .models import Product


@receiver(pre_save, sender=Product)
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

    if not instance.product_id:
        instance.product_id = unique_product_id_generator(instance)


@receiver(post_save, sender=Product)
def post_save_product(sender, instance, created, *args, **kwargs):
    if not created:
        if instance.cartitem_set:
            for item in instance.cartitem_set.all():
                item.refresh_item()
