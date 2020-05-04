import math
import datetime
from decimal import Decimal

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count, Sum, Avg
from django.utils import timezone

from ..billing.models import BillingProfile
from ..carts.models import Cart
from ..products.models import Product
from ..customers.models import Customer
from ..vendors.models import VendorCustomer


ORDER_STATUS_CHOICES = (
    # standard process
    ('created', _('Created')),  # olusturuldu
    ('processing', _('Processing')),  # isleme alindi / isleniyor
    ('booked', _('Booked')),  # paketlendi / hazinrlandi
    ('shipped', _('Shipped')),  # kargolandi
    ('in_transit', _('In Transit')),  # transfer surecinde
    ('delivered', _('Delivered')),  # teslim edildi

    # other situations
    ('refunded', _('Refunded')),  # iade edildi
    ('cancelled', _('Cancelled')),  # iptal edildi
    ('declined', _('Declined')),  # reddedildi
    ('unpaid', _('Unpaid')),  # odenmedi
    ('paid', _('Paid')),  # odendi

    # out of use
    # ('completed', _('Completed')),  # tamamlandi
    # ('processed', _('Processed')),  # islendi
)

PAYMENT_CHOICES = (
    ('cash', _('Cash')),
    ('credit_card', _('Credit Card')),
    ('bank_transfer', _('Bank Transfer')),
)


# OrderShippingInformation modelini reverse lookup olarak baglama. surekli bu fikre kapiliyorsun, once adres girilecek
# sonrasinda EN SON order tamamlanacak!! Suanki hali ideal ve dogru calisiyor.
class OrderShippingInformation(models.Model):
    vendor_customer = models.ForeignKey(VendorCustomer, blank=True, null=True, on_delete=models.SET_NULL,
                                        verbose_name=_('Vendor Customer'))
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_('Customer'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    payment_method = models.CharField(
        blank=True, max_length=120, default='cash', choices=PAYMENT_CHOICES, verbose_name=_('Payment Method'))
    shipping_company = models.CharField(blank=True, max_length=120, verbose_name=_('Shipping Company'))
    shipping_total = models.DecimalField(blank=True, default=Decimal(10.00), max_digits=100, decimal_places=2,
                                         verbose_name=_('Shipping Total'))
    tracking_number = models.CharField(max_length=120, blank=True, verbose_name=_('Tracking Number'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Order Shipping Information'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Order Shipping Information'))

    def __str__(self):
        if self.shipping_company != '' and self.tracking_number != '':
            return '{} | {} | {}'.format(
                self.payment_method,
                self.shipping_company,
                self.tracking_number
            )
        else:
            return '{}'.format(
                self.payment_method
            )

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Order Shipping Information')
        verbose_name_plural = _('Order Shipping Information')


class OrderShippingMovement(models.Model):
    shipping_information = models.ForeignKey(OrderShippingInformation, on_delete=models.CASCADE,
                                             verbose_name=_('Shipping Information'))
    title = models.CharField(max_length=100, blank=False, verbose_name=_('Title'))
    subtitle = models.CharField(max_length=100, blank=False, verbose_name=_('Subtitle (for status info)'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Order Shipping Movement'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Order Shipping Movement'))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Order Shipping Movement')
        verbose_name_plural = _('Order Shipping Movements')


class OrderManagerQuerySet(models.query.QuerySet):

    def get_sales_breakdown(self):
        recent = self.recent().not_refunded()
        recent_data = recent.totals_data()
        recent_cart_data = recent.cart_data()
        shipped = recent.by_status(status='shipped')
        shipped_data = shipped.totals_data()
        paid = recent.by_status(status='paid')
        paid_data = paid.totals_data()
        data = {
            'recent': recent,
            'recent_data': recent_data,
            'recent_cart_data': recent_cart_data,
            'shipped': shipped,
            'shipped_data': shipped_data,
            'paid': paid,
            'paid_data': paid_data
        }
        return data

    def recent(self):
        return self.order_by('-updated_at', '-created_at')

    def totals_data(self):
        return self.aggregate(Sum('total_amount'), Avg('total_amount'))

    def cart_data(self):
        return self.aggregate(
            Sum('productpurchase__line_total'),
            Avg('productpurchase__line_total'),
            Count('productpurchase')
        )

    def not_refunded(self):
        return self.exclude(status='refunded')

    def not_created(self):
        return self.exclude(status='created')

    def by_status(self, status='shipped'):
        return self.filter(status=status)

    def by_request(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)

    def by_date(self):
        now = timezone.now() - datetime.timedelta(days=9)
        return self.filter(updated_at__day__gte=now.day)

    def by_range(self, start_date, end_date=None):
        if end_date is None:
            return self.filter(updated_at__gte=start_date)
        return self.filter(updated_at__gte=start_date).filter(updated_at__lte=end_date)

    def by_weeks_range(self, weeks_ago=7, number_of_weeks=2):
        if number_of_weeks > weeks_ago:
            number_of_weeks = weeks_ago
        days_ago_start = weeks_ago * 7  # days_ago_start = 49
        days_ago_end = days_ago_start - (number_of_weeks * 7)  # days_ago_end = 49 - 14 = 35
        start_date = timezone.now() - datetime.timedelta(days=days_ago_start)
        end_date = timezone.now() - datetime.timedelta(days=days_ago_end)
        return self.by_range(start_date, end_date)

    def products_by_request(self, request):
        qs = self.by_request(request)
        ids_ = [x.productpurchase_set.product.pk for x in qs]
        products_qs = Product.objects.filter(id__in=ids_).distinct()
        return products_qs


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderManagerQuerySet(self.model, using=self._db)

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    # dursun kenarda belki kullanirsin bi gun, suan hic hicbiryerde kullanilmadi.. SILME!!!!
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(
            billing_profile=billing_profile,
            cart=cart_obj,
            active=True,
            status='created'
        )
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                billing_profile=billing_profile,
                cart=cart_obj
            )
            created = True
        return obj, created


# Random, Unique
class Order(models.Model):
    order_id = models.CharField(blank=True, max_length=120, verbose_name=_('Order ID'))
    billing_profile = models.ForeignKey(BillingProfile, null=True, on_delete=models.SET_NULL,
                                        verbose_name=_('Billing Profile'))
    # shipping_information satirini reverse lookup olarak baglama. arada bir bu fikre kapiliyorsun, once adres girilecek
    # ardindan EN SON order tamamlanacak!! Suanki hali ideal ve dogru calisiyor, elleme!.
    # ayrica OneToOneField olarak kalsin. Ikinci order'i girerken adam adresi degistirirse ayni kullaniciyi baz alarak
    # bu sefer onceki order'in log'u da degisecek, cok tehlikeli bir hata olur!!
    shipping_information = models.OneToOneField(OrderShippingInformation, blank=False, null=True,
                                                on_delete=models.SET_NULL, verbose_name=_('Shipping Information'))
    subtotal_amount = models.DecimalField(blank=True, max_digits=100, decimal_places=2, default=Decimal(0.00),
                                          verbose_name=_('Subtotal Amount'))
    total_amount = models.DecimalField(blank=True, max_digits=100, decimal_places=2, default=Decimal(0.00),
                                       verbose_name=_('Total Amount'))
    cart = models.ForeignKey(Cart, null=True, on_delete=models.SET_NULL, verbose_name=_('Cart'))
    status = models.CharField(blank=True, max_length=50, choices=ORDER_STATUS_CHOICES, verbose_name=_('Status'))
    active = models.BooleanField(blank=True, default=True, verbose_name=_('Active'))
    discount_code = models.CharField(blank=True, max_length=120, verbose_name=_('Discount Code'))
    commission_amount = models.DecimalField(blank=True, default=Decimal(0.00), max_digits=120, decimal_places=2,
                                            verbose_name=_('Commission Amount'))
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name=_('IP Address'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Order'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Order'))

    objects = OrderManager()

    def __str__(self):
        return str(self.order_id)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def save(self, *args, **kwargs):
        # if user is vendor
        if hasattr(self.billing_profile, 'user') and hasattr(self.billing_profile.user, 'vendor'):
            # calculate vendor commission amount
            self.commission_amount = self.calculate_vendor_commission_amount()

        # refresh order with addition shipping_total
        self.update_total()

        super(Order, self).save(*args, **kwargs)

        # transfer "cart_item" table to "product_purchase"
        qs = self.cart.cartitem_set.all()
        if qs.count() > 0:
            for x in qs:
                self.productpurchase_set.create(
                    item_id=x.item_id,
                    order=self,
                    product=x.product,
                    product_price=x.product.sale_price,
                    qty=x.qty,
                    line_total=x.product.sale_price * x.qty,
                    refunded=False
                )
                x.delete()
            self.cart.update_cart()

        # if user is vendor, add commission amount to the vendor balance
        if hasattr(self.billing_profile.user, 'vendor'):
            vendor = getattr(self.billing_profile.user, 'vendor')
            order_commission_amount = self.commission_amount
            purchase_obj = self.calculate_purchase_items()
            vendor.total_sales_qty += purchase_obj['total_purchase_product_qty']
            vendor.total_sales_amount += purchase_obj['total_purchase_sales_amount']
            vendor.save()
            vendor.vendorbalance.subtotal_balance += order_commission_amount
            vendor.vendorbalance.save()

            # if discount exists for this vendor, make it passive
            if bool(self.discount_code):
                qs = vendor.vendordiscount_set.all().filter(code=self.discount_code)
                if qs.count() == 1:
                    qs.update(is_active=False)

        # if user is customer
        if hasattr(self.billing_profile.user, 'customer'):
            customer = getattr(self.billing_profile.user, 'customer')

            # if discount code exists for this customer, make it passive
            if bool(self.discount_code):  # if discount code exists
                qs = customer.customerdiscount_set.all().filter(code=self.discount_code)
                if qs.count() == 1:
                    qs.update(is_active=False)

    def calculate_vendor_commission_amount(self):
        """
        do not use directly, use with other methods and check whether not be vendor
        """
        obj = self.cart
        commission_total = obj.subtotal * self.billing_profile.user.vendor.commission_rate
        return commission_total

    def get_status(self):
        if self.status == 'refunded':
            return 'Refunded'
        elif self.status == 'shipped':
            return 'Shipped'
        return 'Shipping Soon'

    def get_purchases(self):
        return self.productpurchase_set.all()

    # with addition shipping_total
    def update_total(self):
        cart_subtotal = self.cart.subtotal
        cart_total = self.cart.total
        shipping_total = self.shipping_information.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        formatted_total = format(new_total, '.2f')
        self.subtotal_amount = cart_subtotal
        self.total_amount = formatted_total
        return {
            'cart_subtotal': cart_subtotal,
            'cart_total': cart_total,
            'shipping_total': shipping_total,
            'new_total': new_total,
            'formatted_total': formatted_total}

    def check_done(self):
        shipping_information_required = True
        if shipping_information_required and self.shipping_information:
            shipping_done = True
        elif shipping_information_required and not self.shipping_information:
            shipping_done = False
        else:
            shipping_done = True
        total = self.total_amount
        if shipping_done and total > Decimal(0.00):
            return True
        return False

    def update_purchases(self):
        for p in self.cart.cartitem_set.all():
            # noinspection All
            obj, created = ProductPurchase.objects.get_or_create(
                order=self,
                product=p.product,
                product_price=p.product.sale_price,
                qty=p.qty,
                line_total=p.product.sale_price * p.qty
            )
        return ProductPurchase.objects.filter(order__order_id=self.order_id).count()

    def mark_paid(self):
        if self.status != 'paid':
            if self.check_done():
                self.status = 'paid'
                self.save()
                self.update_purchases()
        return self.status

    def calculate_purchase_items(self):
        qs = self.productpurchase_set.all()
        total_purchase_product_qty = sum([i.qty for i in qs])  # nays
        total_purchase_amount = Decimal(0.00)
        for i in qs:
            total_purchase_amount += i.line_total
        return {
            'total_purchase_product_qty': total_purchase_product_qty,
            'total_purchase_sales_amount': total_purchase_amount}


class ProductPurchase(models.Model):  # OrderItem
    item_id = models.CharField(max_length=120, blank=True,
                               verbose_name=_('Unique Item ID'))
    order = models.ForeignKey(Order, blank=False, on_delete=models.CASCADE, verbose_name=_('Order'))
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    product_price = models.DecimalField(default=Decimal(0.00), max_digits=25, decimal_places=2,
                                        verbose_name=_('Product Price'))
    qty = models.IntegerField(default=1, verbose_name=_('Quantity'))
    line_total = models.DecimalField(
        blank=True, max_digits=100, decimal_places=2, default=Decimal(0.00), verbose_name=_('Line Total'))
    refunded = models.BooleanField(default=False, verbose_name=_('Refunded'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Product Purchase'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Product Purchase'))

    def __str__(self):
        return self.product.name

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Product Purchase')
        verbose_name_plural = _('Product Purchases')

    def total(self):
        return self.qty * self.product.sale_price

    def name(self):
        return self.product.name

    def sku(self):
        return self.product.sku
