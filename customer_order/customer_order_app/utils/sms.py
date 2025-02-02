import africastalking
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class SMSNotifier:
    def __init__(self):
        try:
            africastalking.initialize(
                username=settings.AFRICASTALKING_USERNAME,
                api_key=settings.AFRICASTALKING_API_KEY
            )
            self.sms = africastalking.SMS
            logger.info("Africa's Talking initialized successfully.")

        except Exception as e:
            logger.error(f"Failed to initialize Africa's Talking: {str(e)}")
            raise

    def send_order_notification(self, phone_number, order_number):
        try:
            # Format phone number
            if not phone_number.startswith('+'):
                phone_number = f'+{phone_number}'

            print(f"\nAttempting to send SMS to {phone_number}")
            message = f"Thank you for your order! Your order #{order_number} has been received and is being processed."

            response = self.sms.send(
                message=message,
                recipients=[phone_number]
            )

            print(f"API Response: {response}")

            if response and 'SMSMessageData' in response:
                message_data = response['SMSMessageData']
                if 'Recipients' in message_data:
                    recipients = message_data['Recipients']
                    if recipients:
                        status = recipients[0].get('status')
                        if status == 'Success':
                            return True, response
                        else:
                            return False, f"Message not delivered. Status: {status}"

            return False, f"Unexpected response format: {response}"

        except Exception as e:
            print(f"\nSMS Error Details:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            return False, f"Error sending SMS: {str(e)}"