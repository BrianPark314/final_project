from django.apps import AppConfig


class MultiappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'multiapp'
