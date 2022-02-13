from django.apps import AppConfig


class AuthorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authors'

    def ready(self):
        import authors.receivers

