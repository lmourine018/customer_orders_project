import africastalking

# Initialize Africa's Talking API
africastalking.initialize(username="sandbox", api_key="atsk_86320dcf752e93ac78507f0021a1fe62d42cd4fd5668faa2277e5cebfa426f8e423e570c")
sms = africastalking.SMS


def send_sms_alert(customer_phone, message):
    """
    Send an SMS to the customer using Africa's Talking API.
    """
    try:
        response = sms.send(message, [customer_phone])
        print("SMS sent successfully:", response)
    except Exception as e:
        print("Error sending SMS:", e)


def add_order(order_details):
    """
    Process the order and send an SMS alert to the customer.
    """
    customer_phone = order_details.get('customer_phone')
    customer_name = order_details.get('customer_name')
    message = f"Dear {customer_name}, your order has been successfully placed. We will notify you with updates. Thank you!"

    send_sms_alert(customer_phone, message)
