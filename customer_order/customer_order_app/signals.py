from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .utils.sms import SMSNotifier


@receiver(post_save, sender=Order)
def send_order_sms(sender, instance, created, **kwargs):
    """
    Signal to send SMS when a new order is created
    """
    if created:  # Only send SMS for new orders
        notifier = SMSNotifier()
        success, response = notifier.send_order_notification(
            phone_number=instance.customer.phone_number,
            order_number=instance.order_number
        )

        # Optional: Log the SMS status
        if not success:
            print(f"Failed to send SMS for order {instance.order_number}: {response}")