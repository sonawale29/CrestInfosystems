from django.apps import AppConfig


class CrestappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CrestApp'

    def ready(self):

        import CrestApp.signals
