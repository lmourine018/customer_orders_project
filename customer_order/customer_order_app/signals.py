import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .utils.sms import SMSNotifier

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Order)
def send_order_sms(sender, instance, created, **kwargs):
    """
    Signal to send SMS when a new order is created
    """
    if created:
        logger.info(f"New order created: {instance.order_number}. Attempting to send SMS.")
        notifier = SMSNotifier()
        success, response = notifier.send_order_notification(
            phone_number=instance.customer.phone_number,
            order_number=instance.order_number
        )

        if not success:
            logger.error(f"Failed to send SMS for order {instance.order_number}: {response}")
        else:
            logger.info(f"SMS sent successfully for order {instance.order_number}.")