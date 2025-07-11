from django.apps import AppConfig


class ArsipConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'arsip'

    def ready(self):
        # Import signals to ensure they are registered
        import arsip.signals
