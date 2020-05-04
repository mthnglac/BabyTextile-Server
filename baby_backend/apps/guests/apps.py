from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class GuestsConfig(AppConfig):
    name = 'baby_backend.apps.guests'
    verbose_name = _('Guests')

    def ready(self):
        from . import signals  # noqa
