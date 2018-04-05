from django.apps import AppConfig


class RrsmiConfig(AppConfig):
    name = 'rrsmi'

    def ready(self):
        from . import signals