from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class GuestVendor(models.Model):
    guest_vendor_id = models.CharField(max_length=120, blank=True, verbose_name=_('Unique Guest Vendor ID'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active/Passive'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Create date of Balance'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Update date of Balance'))

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-updated_at']
        verbose_name = _('Guest Vendor')
        verbose_name_plural = _('Guest Vendors')
