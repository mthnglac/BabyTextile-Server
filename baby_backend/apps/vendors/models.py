import os
import random
from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from baby_backend.utils.utils import calculate_nearest_half, unique_slug_generator

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


def upload_vendor_image_loc(instance, filename):
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
    location = 'vendors/{slug}/{id}/'.format(slug=slug, id=id_)
    return location + final_filename


class Vendor(models.Model):
    vendor_id = models.CharField(max_length=120, blank=True, verbose_name=_('Unique ID'))
    user = models.OneToOneField(User, blank=False, on_delete=models.CASCADE, verbose_name=_('User'))
    tc_number = models.BigIntegerField(blank=False, unique=True, verbose_name=_('Citizenship Number'))
    phone_number = models.CharField(max_length=17, unique=True, blank=False, verbose_name=_('Phone Number'))
    birth_date = models.DateField(blank=True, null=True, verbose_name=_('Birth Date'))
    birth_place = models.CharField(max_length=25, blank=True, verbose_name=_('Birth Place'))
    gender = models.CharField(max_length=25, blank=True, choices=GENDER, verbose_name=_('Gender'))
    dealership_agreement = models.BooleanField(default=False, blank=False, verbose_name=_('Dealership Agreement'))
    sms_request = models.BooleanField(default=False, verbose_name=_('SMS Request'))
    email_request = models.BooleanField(default=False, verbose_name=_('Email Request'))
    commission_rate = models.DecimalField(
        blank=True, default=calculate_nearest_half(Decimal(0.15)), max_digits=3, decimal_places=2,
        verbose_name=_('Commission Rate'))
    total_sales_qty = models.PositiveIntegerField(blank=True, default=0, verbose_name=_('Total Sales Quantity'))
    total_sales_amount = models.DecimalField(
        blank=True, default=Decimal(0.00), max_digits=100, decimal_places=2, verbose_name=_('Total Sales Amount'))
    image = models.ImageField(upload_to=upload_vendor_image_loc, null=True, blank=True, verbose_name=_('Image'))
    slug = models.SlugField(blank=True, unique=True, null=True, verbose_name=_('Slug'))
    sales_quota = models.PositiveSmallIntegerField(blank=True, default=100, verbose_name=_('Sales Quota'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Vendor'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Vendor'))

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Vendor')
        verbose_name_plural = _('Vendors')

    def calculate_total_commission_amount(self):
        qs = self.user.billing_profile.order_set.all()
        if qs.exists():
            commission_total = Decimal(0.00)
            for i in qs:
                commission_total += i.commission_amount
            return commission_total
        return False

    def get_discounts(self):
        qs = self.vendordiscount_set.all()
        if qs.exists():
            return qs.values()
        return False

    def get_delivery_addresses(self):
        qs = self.vendordeliveryaddress_set.all()
        if qs.exists():
            return qs.values()
        return False

    def get_billing_addresses(self):
        qs = self.vendorbillingaddress_set.all()
        if qs.exists():
            return qs.values()
        return False

    def get_bank_information(self):
        query = self.vendorbankaccount
        if query:
            return {
                'account_holder_first_name': query.account_holder_first_name,
                'account_holder_last_name': query.account_holder_last_name,
                'iban': query.iban,
            }
        return False

    def get_balance(self):
        if hasattr(self, 'vendorbalance'):
            return {
                'total': self.vendorbalance.total_balance,
                'subtotal': self.vendorbalance.subtotal_balance,
                'paid': self.vendorbalance.paid_balance,
                'money_demand': self.vendorbalance.money_demand
            }
        else:
            return False

    def get_instagrams(self):
        qs = self.vendorinstagram_set.all()
        if qs.exists():
            return qs.values()
        return False

    def has_instagram(self):
        qs = self.vendorinstagram_set.all()
        if qs.exists():
            return True
        else:
            return False

    def get_current_instagram_information(self):
        if self.has_instagram():
            qs = self.get_instagrams()
            return qs.first()
        return False

    def get_customers(self):
        qs = self.vendorcustomer_set.all()
        if qs.exists():
            return qs.values()
        else:
            return False

    def get_customer_orders(self):
        customers_qs = self.get_customers()
        if customers_qs:
            qs = self.user.billing_profile.order_set.filter(
                shipping_information__vendor_customer__in=customers_qs
            )
            if qs.exists():
                return qs.values()
            else:
                return False
        else:
            return False

    def get_orders(self, status='created'):
        qs = self.user.billing_profile.order_set.filter(status=status)
        if qs.exists():
            return qs.values()
        else:
            return False


class VendorDeliveryAddress(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name=_('Vendor'))
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
        return '{} | {} {} {}'.format(
            self.vendor.user.username, self.address, self.district, self.city)

    class Meta:
        verbose_name = _('Vendor Delivery Address')
        verbose_name_plural = _('Vendor Delivery Address')


class VendorBillingAddress(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name=_('Vendor'))
    title = models.CharField(max_length=30, blank=False, verbose_name=_('Title'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active/Passive'))
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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Address'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Address'))

    def __str__(self):
        return '{} | {} {} {}'.format(
            self.vendor.user.username, self.address, self.district, self.city)

    class Meta:
        verbose_name = _('Vendor Billing Address')
        verbose_name_plural = _('Vendor Billing Address')


class VendorBankAccount(models.Model):
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE, verbose_name=_('Vendor'))
    account_holder_first_name = models.CharField(max_length=20, blank=True, verbose_name=_('Account Holder First Name'))
    account_holder_last_name = models.CharField(max_length=20, blank=True, verbose_name=_('Account Holder Last Name'))
    iban = models.CharField(max_length=26, unique=True, blank=True, null=True, verbose_name=_('IBAN'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Bank Account'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Bank Account'))

    def __str__(self):
        return '{} | {} {} | {}'.format(
            self.vendor,
            self.account_holder_first_name,
            self.account_holder_last_name,
            self.iban
        )

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Vendor Bank Account')
        verbose_name_plural = _('Vendor Bank Accounts')


class VendorInstagram(models.Model):
    vendor = models.ForeignKey(Vendor, verbose_name=_('Vendor'), on_delete=models.CASCADE)
    username = models.CharField(max_length=25, blank=False, verbose_name=_('Username'))
    old_username = models.CharField(max_length=25, blank=True, verbose_name=_('Old Username'))
    followers_qty = models.PositiveIntegerField(blank=True, default=0, verbose_name=_('Count of Followers'))
    old_followers_qty = models.PositiveIntegerField(blank=True, default=0, verbose_name=_('Count of Old Followers'))
    follower_increase_rate = models.DecimalField(
        blank=True, default=Decimal(0.00), max_digits=20, decimal_places=2, verbose_name=_('Follower Increase Rate'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Instagram'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Instagram'))

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-updated_at']
        unique_together = ['vendor', 'username']
        verbose_name = _('Vendor Instagram')
        verbose_name_plural = _('Vendor Instagrams')

    def save(self, *args, **kwargs):
        # self.follower_increase_rate = ((self.followers_qty - self.old_followers_qty) / self.old_followers_qty) * 100
        super(VendorInstagram, self).save(*args, **kwargs)


class VendorDiscountQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class VendorDiscountManager(models.Manager):
    def get_queryset(self):
        return VendorDiscountQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def new(self, vendor_obj, name, discount, valid_until, valid_from=timezone.now, description=None):
        obj = None
        created = False
        try:
            obj = self.model.objects.create(
                vendor=vendor_obj,
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


class VendorDiscount(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name=_('Vendor'))
    name = models.CharField(blank=False, max_length=150, verbose_name=_('Name'))
    description = models.TextField(blank=False, verbose_name=_('Description'))
    code = models.CharField(blank=True, unique=True, null=True, max_length=120, verbose_name=_('Code'))
    discount = models.DecimalField(blank=False, max_digits=3, decimal_places=2, verbose_name=_('Discount'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active/Passive'))
    valid_from = models.DateField(default=timezone.now, verbose_name=_('Valid From'))
    valid_until = models.DateField(blank=False, verbose_name=_('Valid Until'))
    num_uses = models.PositiveSmallIntegerField(default=0, verbose_name=_('Number of times already used'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Discount Code'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Discount Code'))

    objects = VendorDiscountManager()

    def __str__(self):
        return '{} | {}'.format(self.code, self.vendor.user.get_full_name()) \
            if self.vendor.user.first_name and self.vendor.user.last_name \
            else '{} | {}'.format(self.code, self.vendor.user.username)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Vendor Discount')
        verbose_name_plural = _('Vendor Discounts')

    def get_name(self):
        return self.name


class VendorBalance(models.Model):
    vendor = models.OneToOneField(Vendor, blank=False, on_delete=models.CASCADE, verbose_name=_('Vendor'))
    subtotal_balance = models.DecimalField(
        blank=True, default=Decimal(0.00), max_digits=25, decimal_places=2, verbose_name=_('Subtotal Balance'))
    withholding_tax_deduction = models.DecimalField(
        blank=True, default=Decimal(0.00), max_digits=25, decimal_places=2, verbose_name=_('Withholding Tax Deduction'))
    total_balance = models.DecimalField(
        blank=True, default=Decimal(0.00), max_digits=25, decimal_places=2, verbose_name=_('Total Balance'))
    paid_balance = models.DecimalField(
        blank=True, default=Decimal(0.00), max_digits=25, decimal_places=2, verbose_name=_('Paid Balance'))
    money_demand = models.BooleanField(blank=True, default=False, verbose_name=_('Money Demand'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Balance'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Balance'))

    def __str__(self):
        return str(self.vendor.user.username)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Vendor Balance')
        verbose_name_plural = _('Vendor Balances')

    def save(self, *args, **kwargs):
        self.refresh_balance()  # refresh balance for "total_amount" at every save
        super(VendorBalance, self).save(*args, **kwargs)

    def refresh_balance(self):
        self.withholding_tax_deduction = self.subtotal_balance * Decimal(0.15)
        self.total_balance = self.subtotal_balance - self.withholding_tax_deduction
        return {
            'subtotal_balance': self.subtotal_balance,
            'withholding_tax_deduction': self.withholding_tax_deduction,
            'total_balance': self.total_balance,
            'paid_balance': self.paid_balance,
            'money_demand': self.money_demand}


class VendorCustomer(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name=_('Vendor Customer'))
    first_name = models.CharField(max_length=50, blank=False, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=50, blank=False, verbose_name=_('Last Name'))
    phone_number = models.CharField(max_length=17, blank=False, verbose_name=_('Phone Number'))
    city = models.CharField(max_length=30, blank=False, verbose_name=_('City'))
    district = models.CharField(max_length=30, blank=False, verbose_name=_('District'))
    zip_code = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=_('ZIP / Postal Code (Optional)'))
    address = models.TextField(blank=False, verbose_name=_('Address Line'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Vendor'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Vendor'))

    def __str__(self):
        return '{} {}'.format(
            self.first_name,
            self.last_name
        )

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Vendor Customer')
        verbose_name_plural = _('Vendor Customers')
