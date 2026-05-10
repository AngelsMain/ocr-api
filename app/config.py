import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-prod")
    TESSERACT_PATH: str = os.getenv("TESSERACT_PATH", "tesseract")

    # MercadoPago
    MERCADOPAGO_ACCESS_TOKEN: str = os.getenv("MERCADOPAGO_ACCESS_TOKEN", "")

    # Stripe
    STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_PUBLISHABLE_KEY: str = os.getenv("STRIPE_PUBLISHABLE_KEY", "")

    # PayPal
    PAYPAL_CLIENT_ID: str = os.getenv("PAYPAL_CLIENT_ID", "")
    PAYPAL_CLIENT_SECRET: str = os.getenv("PAYPAL_CLIENT_SECRET", "")
    PAYPAL_MODE: str = os.getenv("PAYPAL_MODE", "sandbox")

    MAX_FILE_SIZE: int = 10 * 1024 * 1024
    ALLOWED_FORMATS: list = ["pdf", "jpg", "jpeg", "png"]

settings = Settings()
