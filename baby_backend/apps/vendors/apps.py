from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class VendorsConfig(AppConfig):
    name = 'baby_backend.apps.vendors'
    verbose_name = _('Vendors')

    def ready(self):
        from . import signals  # noqa
