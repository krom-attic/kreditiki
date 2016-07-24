from django.apps import AppConfig


class KreddbConfig(AppConfig):
    name = 'kreddb'

    def ready(self):
        import kreddb.signals
