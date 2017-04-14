from django.apps import AppConfig


class MlsConfig(AppConfig):
    name = 'mls'
    
    def ready(self):
        import mls.signals.handlers #noqa