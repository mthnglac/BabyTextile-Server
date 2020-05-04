from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from decimal import Decimal

from ..products.models import Product
from baby_backend.utils.utils import calculate_nearest_half


class Cart(models.Model):
    cart_id = models.CharField(max_length=120, blank=True, verbose_name=_('Unique Cart ID'))
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name=_('User'))
    qty = models.PositiveSmallIntegerField(default=0, verbose_name=_('Quantity'))
    subtotal = models.DecimalField(
        blank=True, default=Decimal(0.00), max_digits=100, decimal_places=2, verbose_name=_('Subtotal'))
    total = models.DecimalField(blank=True, default=Decimal(0.00), max_digits=100, decimal_places=2,
                                verbose_name=_('Total'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Cart'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Cart'))

    def __str__(self):
        return str(self.pk) \
            if not self.user \
            else '{} | {}'.format(str(self.pk), self.user.username)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def save(self, *args, **kwargs):
        x = self.calculate_cart_items()
        if self.qty != x['total_item_qty'] \
                or self.subtotal != x['subtotal_amount'] \
                or self.total != x['total_amount']:
            self.qty = x['total_item_qty']
            self.subtotal = x['subtotal_amount']
            self.total = x['total_amount']
        super(Cart, self).save(*args, **kwargs)

    def update_cart(self):
        self.subtotal = 0
        self.total = 0
        self.qty = 0
        qs = self.cartitem_set.all()
        if qs.count() > 0:
            for cart_item in qs:
                self.subtotal += cart_item.line_total
            self.total = Decimal(self.subtotal) * Decimal(1.22)
            self.qty = qs.count()
        self.save()
        return {'subtotal': self.subtotal, 'total': self.total, 'qty': self.qty}

    def calculate_cart_items(self):
        qs = self.cartitem_set.all()
        total_item_qty = qs.count()
        total_product_qty = sum([i.qty for i in qs])  # nays
        subtotal_amount = Decimal(0.00)
        for i in qs:
            subtotal_amount += (i.line_total * i.qty)
        total_amount = calculate_nearest_half(Decimal(subtotal_amount) * Decimal(1.22))
        return {
            'total_item_qty': total_item_qty,
            'total_product_qty': total_product_qty,
            'subtotal_amount': subtotal_amount,
            'total_amount': total_amount}


class CartItem(models.Model):
    item_id = models.CharField(max_length=120, blank=True,
                               verbose_name=_('Unique Item ID'))
    cart = models.ForeignKey(Cart, blank=False, on_delete=models.CASCADE,
                             verbose_name=_('Cart'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                verbose_name=_('Product'))
    qty = models.PositiveSmallIntegerField(default=1,
                                           verbose_name=_('Quantity'))
    line_total = models.DecimalField(
        blank=True, max_digits=100, decimal_places=2, default=Decimal(0.00),
        verbose_name=_('Line Total'))
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Create date of Cart'))
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name=_('Update date of Cart'))

    def __str__(self):
        return self.product.name

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')

    def save(self, *args, **kwargs):
        if self.product and self.line_total == 0 \
                or self.product and self.line_total != self.product.sale_price * self.qty:
            self.line_total = self.product.sale_price * self.qty
        super(CartItem, self).save(*args, **kwargs)

    def get_line_total(self):
        return self.qty * self.product.sale_price

    def get_item_name(self):
        return self.product.name

    def get_item_price(self):
        return self.product.sale_price

    def increase_qty(self, qty):
        self.qty += int(qty)
        self.line_total = self.qty * self.product.sale_price
        self.save()
        self.cart.update_cart()
        return self.qty

    def decrease_qty(self, qty):
        self.qty -= int(qty)
        self.line_total = self.qty * self.product.sale_price
        self.save()
        self.cart.update_cart()
        return self.qty

    def remove(self):
        self.delete()
        self.cart.update_cart()
        return True

    def refresh_item(self):
        self.line_total = self.product.sale_price * self.qty
        self.save()
        self.cart.update_cart()
        return {'line_total': self.line_total}
