import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "").strip()
CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET", "").strip()
MODE = os.getenv("PAYPAL_MODE", "sandbox").strip()

print(f"Client ID: {CLIENT_ID[:50]}...")
print(f"Client Secret: {CLIENT_SECRET[:50]}...")
print(f"Mode: {MODE}")

BASE_URL = "https://api.sandbox.paypal.com" if MODE == "sandbox" else "https://api.paypal.com"

auth = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
print(f"Auth header: {auth[:50]}...")

response = requests.post(
    f"{BASE_URL}/v1/oauth2/token",
    headers={
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    },
    data={"grant_type": "client_credentials"}
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
