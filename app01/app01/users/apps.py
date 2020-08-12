from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "app01.users"
    verbose_name = _("用户")

    def ready(self):
        try:
            import app01.users.signals  # noqa F401
        except ImportError:
            pass
