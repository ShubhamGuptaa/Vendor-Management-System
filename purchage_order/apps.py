from django.apps import AppConfig


class PurchageOrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'purchage_order'

    def ready(self):
        import purchage_order.signals  # noqa