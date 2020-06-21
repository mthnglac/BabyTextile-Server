from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from baby_backend.utils.utils import unique_product_unique_id_generator, unique_slug_generator

from .models import (
    Product,
    ProductBrand,
    ProductModel,
    ProductCategory,
    ProductColor,
    ProductSize,
    ProductImage,
    ProductVariant,
)


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


@receiver(pre_save, sender=ProductImage)
def pre_save_product_image(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver(pre_save, sender=ProductBrand)
def pre_save_product_brand(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


@receiver(pre_save, sender=ProductModel)
def pre_save_product_model(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


@receiver(pre_save, sender=ProductColor)
def pre_save_product_color(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


@receiver(pre_save, sender=ProductSize)
def pre_save_product_size(sender, instance, *args, **kwargs):
    if instance.name and not instance.slug:
        instance.slug = slugify(instance.name)


@receiver(pre_save, sender=ProductCategory)
def pre_save_product_category(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


@receiver(pre_save, sender=ProductVariant)
def pre_save_product_variant(sender, instance, *args, **kwargs):
    if not instance.title:
        instance.title = instance.product.name
