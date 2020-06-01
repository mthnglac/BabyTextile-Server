import os
import random
from decimal import Decimal

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager

from baby_backend.utils.utils import (
    calculate_nearest_half,
    get_filename,
    unique_slug_generator,
)

from ..suppliers.models import Supplier


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return 'products/{new_filename}/{final_filename}'.format(
        new_filename=new_filename,
        final_filename=final_filename
    )


class ProductBrand(models.Model):
    slug = models.SlugField(unique=True, null=True, blank=True, verbose_name=_('Slug'))
    name = models.CharField(max_length=30, unique=True, blank=False, verbose_name=_('Brand'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Product Brand'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Product Brand'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Product Brand')
        verbose_name_plural = _('Product Brands')


class ProductModel(models.Model):
    brand = models.ForeignKey(
        ProductBrand, blank=True, on_delete=models.CASCADE, null=True, verbose_name=_('Brand Information'))
    slug = models.SlugField(unique=True, null=True, blank=True, verbose_name=_('Slug'))
    name = models.CharField(max_length=30, unique=True, blank=False, verbose_name=_('Model'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Product Model'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Product Model'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Product Model')
        verbose_name_plural = _('Product Models')


class ProductSize(models.Model):
    slug = models.SlugField(unique=True, null=True, blank=True, verbose_name=_('Slug'))
    name = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name=_('Size Name'))
    start_month = models.PositiveSmallIntegerField(default=0, blank=True, verbose_name=_('Start Month'))
    end_month = models.PositiveSmallIntegerField(default=0, blank=True, verbose_name=_('End Month'))
    age = models.CharField(max_length=10, blank=True, verbose_name=_('Age'))
    size = models.PositiveSmallIntegerField(blank=False, unique=True, verbose_name=_('Size'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Size'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Size'))

    def __str__(self):
        return self.name
        # return '{} - {} | {}'.format(self.start_month, self.end_month, str(self.size)) if not self.age \
        #     else '{} | {}'.format(self.age, str(self.size))

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Product Size')
        verbose_name_plural = _('Product Sizes')


class ProductColor(models.Model):
    slug = models.SlugField(unique=True, null=True, blank=True, verbose_name=_('Slug'))
    name = models.CharField(max_length=15, unique=True, blank=False, verbose_name=_('Color Name'))
    code = models.CharField(max_length=10, blank=True, verbose_name=_('Color Code'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Color'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Color'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Product Color')
        verbose_name_plural = _('Product Colors')


class ProductVAT(models.Model):
    vat_rate = models.DecimalField(max_digits=10, blank=False, unique=True, decimal_places=2,
                                   verbose_name=_('VAT Rate'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Product VAT'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Product VAT'))

    def __str__(self):
        return str(self.vat_rate)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Product VAT')
        verbose_name_plural = _('Product VATs')


class ProductCategory(models.Model):
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name=_('Slug'))
    name = models.CharField(max_length=20, blank=False, unique=True, verbose_name=_('Category'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    active = models.BooleanField(default=True)
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('META Keywords'),
        help_text=_('Comma-delimited set of SEO keywords for meta tag'))
    meta_description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('META Description'),
        help_text=_('Content for description meta tag'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Category'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Category'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Product Category')
        verbose_name_plural = _('Product Categories')


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def search(self, query):
        lookups = (
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(sale_price__icontains=query) |
            Q(tag__name__in=query)
        )
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, pk):
        qs = self.get_queryset().filter(pk=pk)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


class Product(models.Model):
    product_unique_id = models.CharField(max_length=120, blank=True, unique=True, null=True, verbose_name=_('Product ID'))
    name = models.CharField(max_length=150, blank=False, unique=True, verbose_name=_('Name'))
    active = models.BooleanField(default=True, verbose_name=_('Active'))
    featured = models.BooleanField(default=False, verbose_name=_('Featured'))
    best_seller = models.BooleanField(default=False, verbose_name=_('Best Seller'))
    slug = models.SlugField(blank=True, unique=True, null=True, verbose_name=_('Slug'))
    tags = TaggableManager(blank=True)
    brand_information = models.ForeignKey(
        ProductBrand, blank=True, on_delete=models.SET_NULL, null=True,
        verbose_name=_('Brand Information'))
    model_information = models.ForeignKey(
        ProductModel, blank=True, on_delete=models.SET_NULL, null=True,
        verbose_name=_('Model Information'))
    sku = models.CharField(max_length=50, blank=True, verbose_name=_('Stock Keeping Unit'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    # size = models.ManyToManyField(ProductSize, blank=True, verbose_name=_('Size'))
    # color = models.ManyToManyField(ProductColor, blank=True, verbose_name=_('Color'))
    purchase_price = models.DecimalField(
        max_digits=25, decimal_places=2, verbose_name=_('Purchase Price'))
    old_purchase_price = models.DecimalField(
        max_digits=25, decimal_places=2, default=Decimal(0.00), blank=True, verbose_name=_('Old Purchase Price'))
    sale_price = models.DecimalField(max_digits=25, decimal_places=2, verbose_name=_('Sale Price'))
    old_sale_price = models.DecimalField(
        max_digits=25, decimal_places=2, default=Decimal(0.00), blank=True, verbose_name=_('Old Sale Price'))
    vat = models.ForeignKey(ProductVAT, blank=True, null=True, on_delete=models.SET_NULL,
                            verbose_name=_('VAT'))
    category = models.ManyToManyField(ProductCategory, verbose_name=_('Category'))
    supplier = models.ManyToManyField(Supplier, verbose_name=_('Supplier'))
    sold_qty = models.PositiveIntegerField(default=0, blank=True, verbose_name=_('Sold Quantity'))
    purchased_stock = models.PositiveSmallIntegerField(default=0, blank=True, verbose_name=_('Purchased Stock'))
    available_stock = models.IntegerField(default=0, blank=True, verbose_name=_('Available Stock'))
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('META Keywords'),
        help_text=_('Comma-delimited set of SEO keywords for meta tag'))
    meta_description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('META Description'),
        help_text=_('Content for description meta tag'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Product'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Product'))

    objects = ProductManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def save(self, *args, **kwargs):
        self.sale_price = calculate_nearest_half(self.sale_price)
        super(Product, self).save(*args, **kwargs)

    def get_files(self):
        qs = self.productfile_set.all()
        return qs

    def get_product_purchase_count(self):
        return self.productpurchase_set.count()

    def get_billing_profiles(self):
        return self.productpurchase_set.all()

    def get_categories(self):
        return ', '.join([str(i) for i in self.category.all()])


def upload_product_image_loc(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    slug = instance.product.slug
    id_ = instance.id
    if id_ is None:
        Klass = instance.__class__
        qs = Klass.objects.all().order_by('-pk')
        if qs.exists():
            id_ = qs.first().id
        else:
            id_ = 0

    if not slug:
        slug = unique_slug_generator(instance.product)
    location = 'products/{slug}/{id}/'.format(slug=slug, id=id_)
    return location + final_filename


class ProductImageManager(models.Manager):
    def distinct_by_product(self):
        qs = self.model.objects.order_by('product_id', 'created_at').distinct('product_id')
        # -created_at olarak siralanmiyordu. boyle bi cozum yaptim.
        qs_reversed = qs.reverse()
        return qs_reversed


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    name = models.CharField(max_length=120, blank=False, verbose_name=_('Name'))
    slug = models.SlugField(unique=True, null=True, blank=True, verbose_name=_('Slug'))
    image = models.ImageField(upload_to=upload_product_image_loc, null=True, blank=False, verbose_name=_('Image'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of File'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of File'))

    objects = ProductImageManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')


def upload_product_file_loc(instance, filename):
    slug = instance.product.slug
    id_ = instance.id
    if id_ is None:
        Klass = instance.__class__
        qs = Klass.objects.all().order_by('-pk')
        if qs.exists():
            id_ = qs.first().id
        else:
            id_ = 0

    if not slug:
        slug = unique_slug_generator(instance.product)
    location = 'product/{slug}/{id}/'.format(slug=slug, id=id_)
    return location + filename


class ProductFile(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    name = models.CharField(max_length=120, blank=False, verbose_name=_('Name'))
    file = models.FileField(
        upload_to=upload_product_file_loc, blank=False,
        storage=FileSystemStorage(location=settings.PROTECTED_ROOT), verbose_name=_('File'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of File'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of File'))

    def __str__(self):
        return str(self.file.name)

    class Meta:
        ordering = ['updated_at']
        verbose_name = _('Product File')
        verbose_name_plural = _('Product Files')

    @property
    def display_name(self):
        og_name = get_filename(self.file.name)
        if self.name:
            return self.name
        return og_name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, blank=False, on_delete=models.CASCADE, verbose_name=_('Product'))
    title = models.CharField(max_length=20, blank=True, verbose_name=_('Title'))
    color = models.ForeignKey(ProductColor, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_('Color'))
    size = models.ForeignKey(ProductSize, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_('Size'))
    image = models.ForeignKey(ProductImage, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_('Image'))
    qty = models.PositiveSmallIntegerField(default=0, verbose_name=_('Quantity'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Product Variant'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Product Variant'))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Product Variant')
        verbose_name_plural = _('Product Variants')
