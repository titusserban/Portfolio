from django.apps import AppConfig


class DatascienceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'datascience'

    # register the signal
    def ready(self):
        import datascience.signals