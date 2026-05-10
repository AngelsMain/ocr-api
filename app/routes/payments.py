from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.payments import payment_manager

router = APIRouter()

class PlanUpgrade(BaseModel):
    user_id: str
    plan: str
    provider: str  # "stripe", "paypal", "mercadopago"

class PaymentResponse(BaseModel):
    success: bool
    provider: str | None = None
    message: str = ""
    client_secret: str | None = None
    payment_intent_id: str | None = None
    preference_id: str | None = None
    init_point: str | None = None
    redirect_url: str | None = None
    payment_id: str | None = None

@router.post("/create-payment")
async def create_payment(request: PlanUpgrade):
    try:
        result = payment_manager.create_payment(
            request.user_id,
            request.plan,
            request.provider
        )

        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])

        provider = result.get("provider", "free")

        if provider == "free":
            return PaymentResponse(
                success=True,
                provider="free",
                message="Plan Gratis activado"
            )
        elif provider == "stripe":
            return PaymentResponse(
                success=True,
                provider="stripe",
                message="Intent de pago creado",
                client_secret=result.get("client_secret"),
                payment_intent_id=result.get("payment_intent_id")
            )
        elif provider == "paypal":
            return PaymentResponse(
                success=True,
                provider="paypal",
                message="Pagador PayPal creado",
                payment_id=result.get("payment_id"),
                redirect_url=result.get("redirect_url")
            )
        elif provider == "mercadopago":
            return PaymentResponse(
                success=True,
                provider="mercadopago",
                message="Preferencia de pago creada",
                preference_id=result.get("preference_id"),
                init_point=result.get("init_point")
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/plans")
async def get_plans():
    return {
        "planes": {
            "free": {
                "precio_usd": 0,
                "precio_cop": 0,
                "requests": 100,
                "nombre": "Plan Gratis"
            },
            "pro": {
                "precio_usd": 29,
                "precio_cop": 29000,
                "requests": 10000,
                "nombre": "Plan Pro"
            },
            "enterprise": {
                "precio_usd": 299,
                "precio_cop": 299000,
                "requests": "Ilimitado",
                "nombre": "Plan Enterprise"
            }
        },
        "proveedores_disponibles": ["stripe", "paypal", "mercadopago", "free"]
    }
