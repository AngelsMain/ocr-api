# 💳 OCR API - Guía de Pagos con PayPal

Tu API acepta pagos **solo con PayPal** de momento.

---

## 📋 Setup de PayPal

### 1. Crear cuenta PayPal Developer

1. Ir a https://developer.paypal.com
2. Login con tu cuenta PayPal
3. Si no tienes: crear en https://www.paypal.com/co

### 2. Obtener credenciales Sandbox

1. En Dashboard → **Apps & Credentials**
2. Asegúrate que estés en **Sandbox** (arriba)
3. Busca tu aplicación "ocr-api"
4. Copia:
   - **Client ID**
   - **Secret**

### 3. Guardar en `.env`

```env
PAYPAL_CLIENT_ID=Tu_Client_ID_Aqui
PAYPAL_CLIENT_SECRET=Tu_Secret_Aqui
PAYPAL_MODE=sandbox
```

### 4. Reiniciar Docker

```bash
docker-compose down
docker-compose up --build
```

---

## 🧪 Probar pagos

### Ver planes disponibles

```bash
curl http://localhost:8000/api/v1/payments/plans
```

Respuesta:
```json
{
  "planes": {
    "free": {"precio_usd": 0, "requests": 100},
    "pro": {"precio_usd": 29, "requests": 10000},
    "enterprise": {"precio_usd": 299, "requests": "Ilimitado"}
  },
  "proveedores_disponibles": ["paypal"]
}
```

### Crear pago con PayPal

```bash
curl -X POST http://localhost:8000/api/v1/payments/create-payment \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "usuario_test",
    "plan": "pro",
    "provider": "paypal"
  }'
```

**Respuesta correcta:**
```json
{
  "success": true,
  "provider": "paypal",
  "message": "Pagador PayPal creado",
  "order_id": "7C679141H36...",
  "redirect_url": "https://www.sandbox.paypal.com/checkoutnow?token=EC-..."
}
```

---

## 💰 Flujo de pago

### Paso 1: Usuario solicita pago
```
Tu frontend → GET /api/v1/payments/create-payment
```

### Paso 2: Recibe link PayPal
```
Tu API → retorna "redirect_url"
```

### Paso 3: Usuario hace click
```
redirect_url → PayPal Sandbox → Paga
```

### Paso 4: Confirmación
```
PayPal → Webhook de confirmación (implementar después)
```

---

## 🚨 Solucionar errores

### Error: "No se pudo autenticar con PayPal"

**Causa:** Credenciales mal configuradas

**Solución:**
1. Verifica que `.env` tenga credenciales correctas
2. Asegúrate que están en **Sandbox** (no Live)
3. Reinicia Docker: `docker-compose restart`

### Error: "Invalid Client ID"

**Causa:** Client ID incorrecto o no coincide con Secret

**Solución:**
1. Ve a https://developer.paypal.com
2. Copia las credenciales nuevamente
3. Asegúrate de copiar exactamente (sin espacios)

### Error: "HTTP 401"

**Causa:** Secret incorrecto

**Solución:**
1. Regenera las credenciales en PayPal Developer
2. Copia nuevamente Client ID + Secret

---

## 🌐 Pasar a Producción (Live)

### 1. Crear credenciales Live

En PayPal Developer:
1. Ir a **Apps & Credentials**
2. Cambiar a **Live** (arriba)
3. Crear aplicación (si no existe)
4. Copiar credenciales Live

### 2. Actualizar `.env`

```env
PAYPAL_CLIENT_ID=Tu_Live_Client_ID
PAYPAL_CLIENT_SECRET=Tu_Live_Secret
PAYPAL_MODE=live
```

### 3. Actualizar URLs de retorno

En `app/payments.py`, actualiza:
```python
"return_url": "https://tu-api-real.com/success",
"cancel_url": "https://tu-api-real.com/cancel"
```

### 4. Desplegar a Render

Ver `DEPLOYMENT.md`

---

## 💵 Recibir dinero en tu banco

### 1. Dinero llega a PayPal
- Cliente paga $29 USD
- PayPal descuenta comisión: $0.84 USD (2.9% + $0.30)
- Tú recibís: $28.16 USD

### 2. Retirar a tu banco colombiano

1. Ir a https://www.paypal.com/co
2. Login en tu cuenta
3. Ir a **Billetera** → **Dinero**
4. Click en **"Transferir dinero"**
5. Seleccionar cuenta bancaria
6. Ingresar monto en USD
7. PayPal convierte a COP
8. Confirmar

**Tiempo:** 1-3 días hábiles

---

## 📊 Planes de precios

| Plan | Precio USD | Requests/mes | Uso |
|------|-----------|--------------|-----|
| **Free** | $0 | 100 | Pruebas |
| **Pro** | $29 | 10,000 | Producción |
| **Enterprise** | $299 | Ilimitado | Empresas |

---

## ❓ Preguntas frecuentes

**P: ¿Puedo probar sin dinero real?**
R: Sí, con Sandbox mode (modo actual). Usa credenciales de prueba.

**P: ¿Cuándo recibo el dinero?**
R: 1-3 días después de que el cliente pague.

**P: ¿Cuánto me cobra PayPal?**
R: 2.9% + $0.30 USD por transacción.

**P: ¿Puedo agregar MercadoPago después?**
R: Sí, cuando tu cuenta en MercadoPago se verifique, agregamos el código.

---

## 🚀 Próximo paso

Desplegar en **Render** para que usuarios reales puedan pagar:
```bash
Ver DEPLOYMENT.md
```
