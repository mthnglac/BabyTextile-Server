from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class BillingProfileQuerySet(models.query.QuerySet):
    def all_vendor(self):
        vendor_list = []
        for i in self:
            if hasattr(i.user, 'vendor'):
                vendor_list.append(i.user.vendor.user.username)
            else:
                continue
        return vendor_list

    def all_customer(self):
        customer_list = []
        for i in self:
            if hasattr(i.user, 'customer'):
                customer_list.append(i.user.customer.user.username)
            else:
                continue
        return customer_list


class BillingProfileManager(models.Manager):
    def get_queryset(self):
        return BillingProfileQuerySet(self.model, using=self._db)

    def new_or_get(self, request):
        created = False
        obj = None
        user = request.user
        if user.is_authenticated:
            # logged in user checkout; remember payment stuff
            obj, created = self.model.objects.get_or_create(user=user)
        else:
            pass
        return obj, created

    def vendor_profiles(self):
        return self.get_queryset().all_vendor()

    def customer_profiles(self):
        return self.get_queryset().all_customer()


class BillingProfile(models.Model):
    user = models.OneToOneField(User, blank=False, related_name='billing_profile',
                                on_delete=models.CASCADE, verbose_name=_('User'))
    is_active = models.BooleanField(blank=True, default=True, verbose_name=_('Active/Passive'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Billing Profile'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Billing Profile'))

    objects = BillingProfileManager()

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Billing Profile')
        verbose_name_plural = _('Billing Profiles')


class ChargeManager(models.Manager):
    def do(self, billing_profile, order_obj):  # Charge.objects.do()
        new_charge_obj = self.model(
            billing_profile=billing_profile,
            # paid=paid,
            # refunded=refunded,
            # outcome=outcome,
            # outcome_type=outcome['type'],
            # seller_message=outcome.get('seller_message'),
            # risk_level=outcome.get('risk_level'),
        )
        new_charge_obj.save()
        return new_charge_obj


class Charge(models.Model):
    billing_profile = models.ForeignKey(
        BillingProfile, blank=False, on_delete=models.CASCADE, verbose_name=_('Billing Profile'))
    paid = models.BooleanField(default=False, verbose_name=_('Paid'))
    refunded = models.BooleanField(default=False, verbose_name=_('Refunded'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Charge'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Charge'))

    objects = ChargeManager()

    def __str__(self):
        return self.billing_profile.user.get_full_name() \
            if self.billing_profile.user.first_name and self.billing_profile.user.last_name \
            else self.billing_profile.user.username

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Charge')
        verbose_name_plural = _('Charges')
