from django.apps import AppConfig


class SafeAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'safe_admin'
