from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AccountsConfig(AppConfig):
    name = 'baby_backend.apps.accounts'
    verbose_name = _('Accounts')
