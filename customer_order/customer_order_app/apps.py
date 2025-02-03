from django.apps import AppConfig


class CustomerConfig(AppConfig):
    # Set the default auto field for models
    default_auto_field = 'django.db.models.BigAutoField'

    # Name of the app
    name = 'customer_order_app'

    def ready(self):
        # Import signals to ensure they are registered
        import customer_order_app.signals


# Set the default app config for backward compatibility
# default_app_config = 'customer_order_app.apps.CustomerConfig'