import mercadopago
import stripe
from app.config import settings

mp_client = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentManager:
    PRICING_PLANS = {
        "free": {"price_usd": 0, "price_cop": 0, "requests": 100, "name": "Plan Gratis"},
        "pro": {"price_usd": 29, "price_cop": 29000, "requests": 10000, "name": "Plan Pro"},
        "enterprise": {"price_usd": 299, "price_cop": 299000, "requests": float('inf'), "name": "Plan Enterprise"}
    }

    @staticmethod
    def create_paypal_payment(user_id: str, plan: str):
        """Versión de prueba - retorna un link de demostración"""
        try:
            plan_info = PaymentManager.PRICING_PLANS.get(plan)
            if not plan_info:
                return {"success": False, "error": "Plan no encontrado"}

            amount = str(plan_info["price_usd"])
            if float(amount) == 0:
                return {"success": True, "provider": "free", "plan": plan}

            # VERSIÓN DE PRUEBA - Sin llamada a PayPal
            # En producción, esto llamaría a PayPal API
            return {
                "success": True,
                "provider": "paypal",
                "message": f"Pago de ${amount} USD creado",
                "order_id": "DEMO-123456",
                "redirect_url": f"https://www.sandbox.paypal.com/checkoutnow?token=DEMO_TOKEN_{user_id}_{plan}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def create_mercadopago_preference(user_id: str, plan: str):
        try:
            plan_info = PaymentManager.PRICING_PLANS.get(plan)
            if not plan_info:
                return {"success": False, "error": "Plan no encontrado"}

            amount = plan_info["price_cop"]
            if amount == 0:
                return {"success": True, "provider": "free", "plan": plan}

            preference_data = {
                "items": [{
                    "title": plan_info["name"],
                    "quantity": 1,
                    "unit_price": amount / 100
                }],
                "metadata": {"user_id": user_id, "plan": plan},
                "currency_id": "COP"
            }
            resp = mp_client.preference().create(preference_data)
            if resp["status"] == 201:
                return {
                    "success": True,
                    "provider": "mercadopago",
                    "preference_id": resp["response"]["id"],
                    "init_point": resp["response"]["init_point"]
                }
            return {"success": False, "error": "Error en MercadoPago"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def create_stripe_payment_intent(user_id: str, plan: str):
        try:
            plan_info = PaymentManager.PRICING_PLANS.get(plan)
            if not plan_info:
                return {"success": False, "error": "Plan no encontrado"}

            amount_cents = int(plan_info["price_usd"] * 100)
            if amount_cents == 0:
                return {"success": True, "provider": "free", "plan": plan}

            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency="usd",
                metadata={"user_id": user_id, "plan": plan}
            )
            return {
                "success": True,
                "provider": "stripe",
                "client_secret": intent.client_secret,
                "payment_intent_id": intent.id
            }
        except stripe.error.StripeError as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_plan_details(plan: str):
        return PaymentManager.PRICING_PLANS.get(plan, PaymentManager.PRICING_PLANS["free"])

    @staticmethod
    def create_payment(user_id: str, plan: str, provider: str):
        if provider == "mercadopago":
            return PaymentManager.create_mercadopago_preference(user_id, plan)
        elif provider == "stripe":
            return PaymentManager.create_stripe_payment_intent(user_id, plan)
        elif provider == "paypal":
            return PaymentManager.create_paypal_payment(user_id, plan)
        else:
            return {"success": False, "error": "Proveedor no soportado"}

payment_manager = PaymentManager()
