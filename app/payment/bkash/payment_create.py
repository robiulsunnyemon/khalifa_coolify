import requests
from app.payment.bkash.bkash_payment_token_generation import APP_KEY

def create_payment(token, amount, invoice_id="12345"):

    url = "https://checkout.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/payment/create"
    headers = {
        "Authorization": token,
        "X-APP-Key": APP_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "amount": str(amount),
        "currency": "BDT",
        "intent": "sale",
        "merchantInvoiceNumber": invoice_id
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()
