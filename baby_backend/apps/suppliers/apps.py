from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SuppliersConfig(AppConfig):
    name = 'baby_backend.apps.suppliers'
    verbose_name = _('Suppliers')

    def ready(self):
        from . import signals  # noqa
