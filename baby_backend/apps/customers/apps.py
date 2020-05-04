from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CustomersConfig(AppConfig):
    name = 'baby_backend.apps.customers'
    verbose_name = _('Customers')

    def ready(self):
        from . import signals  # noqa
