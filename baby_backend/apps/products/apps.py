from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ProductsConfig(AppConfig):
    name = 'baby_backend.apps.products'
    verbose_name = _('Products')

    def ready(self):
        from . import signals  # noqa
