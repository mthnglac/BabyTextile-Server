from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class OrdersConfig(AppConfig):
    name = 'baby_backend.apps.orders'
    verbose_name = _('Orders')

    def ready(self):
        from . import signals  # noqa
