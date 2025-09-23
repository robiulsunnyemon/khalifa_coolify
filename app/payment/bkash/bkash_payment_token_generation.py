import requests

BKASH_BASE_URL = "https://checkout.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/token/grant"  # Sandbox
APP_KEY = "আপনার_APP_KEY"
APP_SECRET = "আপনার_APP_SECRET"

def get_bkash_token():
    headers = {
        "username": "আপনার_মারচেন্ট_ইউজারনেম",
        "password": "আপনার_মারচেন্ট_পাসওয়ার্ড",
        "Content-Type": "application/json"
    }
    data = {
        "app_key": APP_KEY,
        "app_secret": APP_SECRET
    }

    response = requests.post(BKASH_BASE_URL, json=data, headers=headers)
    return response.json()
