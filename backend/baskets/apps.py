from django.apps import AppConfig


class BasketsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'baskets'

    def ready(self):
        import baskets.signals 
