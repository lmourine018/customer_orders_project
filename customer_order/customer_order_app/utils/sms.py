import africastalking
from django.conf import settings

class SMSNotifier:
    def __init__(self):
        # Initialize Africa's Talking
        africastalking.initialize(
            username=settings.AFRICASTALKING_USERNAME,
            api_key=settings.AFRICASTALKING_API_KEY
        )
        self.sms = africastalking.SMS

    def send_order_notification(self, phone_number, order_number):
        """
        Send SMS notification for new order
        """
        try:
            message = f"Thank you for your order! Your order #{order_number} has been received and is being processed."
            response = self.sms.send(
                message=message,
                recipients=[phone_number],
                sender_id=settings.AFRICASTALKING_SENDER_ID
            )
            return True, response
        except Exception as e:
            return False, str(e)