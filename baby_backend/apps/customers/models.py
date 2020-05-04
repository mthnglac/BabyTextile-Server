import os
import random

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from baby_backend.utils.utils import unique_slug_generator

BILLING_TYPE = (
    ('individual', _('Individual')),
    ('corporate', _('Corporate'))
)

GENDER = (
    ('male', _('Male')),
    ('female', _('Female'))
)


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_customer_image_loc(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    slug = instance.slug
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
    location = 'customers/{slug}/{id}/'.format(slug=slug, id=id_)
    return location + final_filename


class Customer(models.Model):
    customer_id = models.CharField(blank=True, max_length=120, verbose_name=_('Customer ID'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    tc_number = models.BigIntegerField(blank=False, verbose_name=_('Citizenship Number'))  # check unique from FrontEnd?
    gender = models.CharField(max_length=25, blank=True, choices=GENDER, verbose_name=_('Gender'))
    birth_date = models.DateField(blank=True, null=True, verbose_name=_('Birth Date'))
    phone_number = models.CharField(max_length=17, blank=False, verbose_name=_('Phone Number'))
    sms_request = models.BooleanField(default=False, verbose_name=_('SMS Request'))
    email_request = models.BooleanField(default=False, verbose_name=_('Email Request'))
    image = models.ImageField(upload_to=upload_customer_image_loc, null=True, blank=True, verbose_name=_('Image'))
    slug = models.SlugField(blank=True, unique=True, null=True, verbose_name=_('Slug'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Customer'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Customer'))

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    def get_addresses(self):
        qs = self.customerdeliveryaddress_set.all()
        if qs.exists():
            address_list = [(x.is_active, x.address,  x.zip_code, x.district, x.city)
                            for i in list(zip(qs)) for x in i]
            return address_list
        return False

    def get_active_address(self):
        qs = self.customerdeliveryaddress_set.filter(is_active=True)
        if qs.count() == 1:
            address_list = qs.first()
            return address_list
        return False


class CustomerDeliveryAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_('Customer'))
    title = models.CharField(max_length=30, blank=False, verbose_name=_('Title'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active/Passive'))
    address = models.TextField(blank=False, verbose_name=_('Address Line'))
    zip_code = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=_('ZIP / Postal Code'))
    district = models.CharField(max_length=30, blank=False, verbose_name=_('District'))
    city = models.CharField(max_length=30, blank=False, verbose_name=_('City'))
    country = models.CharField(max_length=30, blank=True, default='Turkey', verbose_name=_('Country'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Address'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Address'))

    def __str__(self):
        return '{} | {}'.format(
            self.customer.user.username,
            self.address
        )

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Customer Delivery Address')
        verbose_name_plural = _('Customer Delivery Addresses')


class CustomerBillingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_('Customer'))
    title = models.CharField(max_length=30, blank=False, verbose_name=_('Title'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active/Passive'))
    abc = models.Choices
    address = models.TextField(blank=False, verbose_name=_('Address Line'))
    zip_code = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=_('ZIP / Postal Code'))
    district = models.CharField(max_length=30, blank=False, verbose_name=_('District'))
    city = models.CharField(max_length=30, blank=False, verbose_name=_('City'))
    country = models.CharField(max_length=30, blank=True, default='Turkey', verbose_name=_('Country'))
    billing_type = models.CharField(blank=True, default='individual', max_length=50, choices=BILLING_TYPE,
                                    verbose_name=_('Billing Type'))
    company_name = models.CharField(blank=True, max_length=100, verbose_name=_('Company Name'))
    tax_number = models.BigIntegerField(blank=True, default=0, verbose_name=_('Tax Number'))
    tax_office = models.CharField(max_length=100, blank=True, verbose_name=_('Tax Office'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Billing Address'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Billing Address'))

    def __str__(self):
        return '{} | {} {} {}'.format(
            self.customer.user.username, self.address, self.district, self.city)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Customer Billing Address')
        verbose_name_plural = _('Customer Billing Addresses')


class CustomerDiscountQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class CustomerDiscountManager(models.Manager):
    def get_queryset(self):
        return CustomerDiscountQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def new(self, customer_obj, name, discount, valid_until, valid_from=timezone.now, description=None):
        obj = None
        created = False
        try:
            obj = self.model.objects.create(
                customer=customer_obj,
                name=name,
                description=description,
                discount=discount,
                valid_from=valid_from,
                valid_until=valid_until,
            )
            created = True
        except IndexError:
            pass
        return obj, created


class CustomerDiscount(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_('Customer'))
    name = models.CharField(blank=False, max_length=150, verbose_name=_('Name'))
    description = models.TextField(blank=False, verbose_name=_('Description'))
    code = models.CharField(blank=True, unique=True, null=True, max_length=120, verbose_name=_('Code'))
    discount = models.DecimalField(blank=False, max_digits=3, decimal_places=2, verbose_name=_('Discount'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active/Passive'))
    valid_from = models.DateField(default=timezone.now, blank=True, verbose_name=_('Valid From'))
    valid_until = models.DateField(blank=False, verbose_name=_('Valid Until'))
    num_uses = models.PositiveSmallIntegerField(default=0, verbose_name=_('Number of times already used'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Discount Code'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Discount Code'))

    objects = CustomerDiscountManager()

    def __str__(self):
        return '{} | {}'.format(self.code, self.customer.user.get_full_name()) \
            if self.customer.user.first_name and self.customer.user.last_name \
            else '{} | {}'.format(self.code, self.customer.user.username)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Customer Discount')
        verbose_name_plural = _('Customer Discounts')

    def get_name(self):
        return self.name
