import os
import africastalking
from django.conf import settings


class SMSNotifier:
    def __init__(self):
        try:
            # Get credentials with detailed validation
            self.username = getattr(settings, 'AFRICASTALKING_USERNAME', None)
            self.api_key = getattr(settings, 'AFRICASTALKING_API_KEY', None)

            print("\nInitial Credential Check:")
            print(f"Username type: {type(self.username)}")
            print(f"Username value: {self.username}")
            print(f"API key starts with: {self.api_key[:8]}...")

            # Validate and clean username
            if not self.username or not isinstance(self.username, str):
                raise ValueError("Username must be a non-empty string")

            self.username = self.username.strip().lower()  # Normalize username
            if self.username != 'sandbox':
                raise ValueError("For testing, username must be 'sandbox'")

            # Validate API key
            if not self.api_key or not isinstance(self.api_key, str):
                raise ValueError("API key must be a non-empty string")

            self.api_key = self.api_key.strip()
            if not self.api_key.startswith('atsk_'):
                raise ValueError("Invalid API key format - should start with 'atsk_'")

            print("\nTrying to initialize Africa's Talking...")
            # Initialize with validated credentials
            africastalking.initialize(
                username=self.username,
                api_key=self.api_key
            )
            print("Basic initialization completed")

            print("\nGetting SMS service...")
            self.sms = africastalking.SMS
            print("SMS service obtained")

            print("\nVerifying application data...")
            # Try to get application data without storing it
            africastalking.Application.fetch_application_data()
            print("Application data verified")

        except Exception as e:
            print("\nError Details:")
            print(f"Username (final): '{self.username}'")
            print(f"API key length: {len(self.api_key)} characters")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
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


if __name__ == "__main__":
    try:
        print("Setting up Django configuration...")
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "customer_order.settings")
        settings.configure(
            AFRICASTALKING_USERNAME='sandbox',
            AFRICASTALKING_API_KEY='atsk_55be84f038ab74e599f195923af33e10b54abe6ff7ac540e9d42e9da2740a357691b7f65'
        )

        print("\nCreating SMS Notifier...")
        notifier = SMSNotifier()

        phone_number = "254796414995"
        order_number = "ORDER123"

        print("\nSending test SMS...")
        success, response = notifier.send_order_notification(phone_number, order_number)

        print(f"\nFinal Result:")
        print(f"SMS sending {'successful' if success else 'failed'}: {response}")

    except Exception as e:
        print(f"\nFailed to initialize or send SMS: {str(e)}")