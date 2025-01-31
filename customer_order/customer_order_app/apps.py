from django.apps import AppConfig


class CustomerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customer_order_app'

    def ready(self):
        import customer_order_app.signals
