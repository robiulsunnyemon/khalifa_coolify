import requests
from app.payment.bkash.bkash_payment_token_generation import APP_KEY

def execute_payment(token, payment_id):
    url = f"https://checkout.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/payment/execute/{payment_id}"
    headers = {
        "Authorization": token,
        "X-APP-Key": APP_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers)
    return response.json()
