from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CartsConfig(AppConfig):
    name = 'baby_backend.apps.carts'
    verbose_name = _('Carts')

    def ready(self):
        from . import signals  # noqa
