from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class BillingConfig(AppConfig):
    name = 'baby_backend.apps.billing'
    verbose_name = _('Billing')

    def ready(self):
        from . import signals  # noqa
