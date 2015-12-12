from django.apps import AppConfig


class Config(AppConfig):
    name = 'sk_map'

    def ready(self):
        import sk_map.signals