# Configuración de Pagos (Stripe + PayPal + MercadoPago)

Tu API ahora acepta pagos de **3 proveedores** simultáneamente:

---

## 1️⃣ MercadoPago (Colombia) 🇨🇴

**Mejor para**: Usuarios de Colombia/Latam

### Setup:
1. Ir a https://www.mercadopago.com.co
2. Vender → Integraciones → Credenciales
3. Copiar **Access Token** de Producción
4. Pegar en `.env`:
```
MERCADOPAGO_ACCESS_TOKEN=APP_USR_xxxxxxxxxx
```

### Precios (COP):
- Free: $0
- Pro: $29,000
- Enterprise: $299,000

---

## 2️⃣ PayPal (Internacional) 🌍

**Mejor para**: Usuarios globales, Colombia

### Crear cuenta:
1. Ir a https://www.paypal.com/co
2. Crear cuenta de Negocio
3. Ir a Configuración → Credenciales
4. Crear Aplicación → Copiar Client ID y Secret
5. Pegar en `.env`:
```
PAYPAL_CLIENT_ID=xxxxxxxxxxxxxxxx
PAYPAL_CLIENT_SECRET=xxxxxxxxxxxxxxxx
PAYPAL_MODE=sandbox  # Cambiar a "live" en producción
```

### Precios (USD):
- Free: $0
- Pro: $29
- Enterprise: $299

---

## 3️⃣ Stripe (Internacional) 🌐

**Mejor para**: Usuarios de USA, Europa

### Crear cuenta en otro país:
Como Stripe no soporta Colombia directamente, opciones:

**A. Abrir empresa en otro país:**
- España, México, Argentina, etc.
- Stripe sí funciona ahí
- Dinero va a cuenta del otro país

**B. Usar verificación alternativa:**
- Algunos países aceptan con verificación extra
- Contactar Stripe Support

### Si logras habilitar:
1. Ir a https://dashboard.stripe.com
2. Developers → API keys
3. Copiar Secret Key y Publishable Key
4. Pegar en `.env`:
```
STRIPE_SECRET_KEY=sk_test_xxxxxxxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxxxxx
```

### Precios (USD):
- Free: $0
- Pro: $29
- Enterprise: $299

---

## 📡 Usar en tu API

### Ver planes disponibles:
```bash
curl http://localhost:8000/api/v1/payments/plans
```

### Crear pago con MercadoPago:
```bash
curl -X POST http://localhost:8000/api/v1/payments/create-payment \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "usuario123",
    "plan": "pro",
    "provider": "mercadopago"
  }'
```

Respuesta:
```json
{
  "success": true,
  "provider": "mercadopago",
  "init_point": "https://www.mercadopago.com.co/checkout/xxx"
}
```

### Crear pago con PayPal:
```bash
curl -X POST http://localhost:8000/api/v1/payments/create-payment \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "usuario123",
    "plan": "pro",
    "provider": "paypal"
  }'
```

Respuesta:
```json
{
  "success": true,
  "provider": "paypal",
  "redirect_url": "https://www.sandbox.paypal.com/checkout/xxx"
}
```

### Crear pago con Stripe:
```bash
curl -X POST http://localhost:8000/api/v1/payments/create-payment \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "usuario123",
    "plan": "pro",
    "provider": "stripe"
  }'
```

Respuesta:
```json
{
  "success": true,
  "provider": "stripe",
  "client_secret": "pi_xxx"
}
```

---

## 💡 Recomendación para Colombia

**Usa MercadoPago + PayPal:**
- MercadoPago: usuarios locales (COP)
- PayPal: usuarios internacionales (USD)
- Stripe: si logras habilitarlo

Esto maximiza tus conversiones sin complicaciones de Stripe.

---

## 🔄 Recibir dinero

| Provider | Comisión | Moneda | Retiro |
|----------|----------|--------|--------|
| MercadoPago | 2.99% + $300 | COP | Cuenta bancaria CO |
| PayPal | 3.49% | USD | PayPal Wallet + retiro |
| Stripe | 2.9% + $0.30 | USD | Cuenta bancaria CO |

---

## ⚠️ Notas importantes

- **Sandbox vs Production**: Cambiar `PAYPAL_MODE` a "live" en producción
- **Webhooks**: Implementar webhooks para confirmar pagos recibidos
- **Base de datos**: Guardar user_id → plan → payment_status para tracking
- **URLs de retorno**: Actualizar `redirect_urls` en `payments.py` con tus dominios reales
