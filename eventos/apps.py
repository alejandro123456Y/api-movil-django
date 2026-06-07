from django.apps import AppConfig


class EventosConfig(AppConfig):
    name = 'eventos'

    def ready(self):
        import eventos.signals  # noqa: F401
