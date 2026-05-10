# Configurar MercadoPago (Colombia)

## 1. Crear cuenta MercadoPago

1. Ir a https://www.mercadopago.com.co
2. Click en "Vende con Mercado Pago"
3. Crear cuenta con email y contraseña
4. Verificar email

## 2. Obtener Access Token

### Opción A: Desde Dashboard (Recomendado)
1. Iniciar sesión en https://www.mercadopago.com.co
2. Ir a **Configuración** → **Integraciones** → **Credenciales**
3. Copiar el **Access Token** de Producción

### Opción B: Desde Aplicaciones
1. Ir a **Mis integraciones** → **Mis aplicaciones**
2. Crear nueva aplicación
3. Copiar **Token de acceso**

## 3. Actualizar .env

Reemplaza en tu archivo `.env`:
```
MERCADOPAGO_ACCESS_TOKEN=APP_USR_xxxxxxxxxxxxxxxxxx
```

## 4. Precios en COP (Pesos Colombianos)

El proyecto ya está configurado con precios en COP:
- **Free**: $0 - 100 requests/mes
- **Pro**: $29,000 COP - 10,000 requests/mes  
- **Enterprise**: $299,000 COP - Ilimitado

## 5. Probar Pagos

```bash
curl -X GET http://localhost:8000/api/v1/payments/plans
```

Respuesta con precios en COP:
```json
{
  "planes": {
    "free": {"precio_cop": 0, "requests": 100},
    "pro": {"precio_cop": 29000, "requests": 10000},
    "enterprise": {"precio_cop": 299000, "requests": "Ilimitado"}
  }
}
```

## 6. Crear Preferencia de Pago

```bash
curl -X POST http://localhost:8000/api/v1/payments/upgrade-plan \
  -H "Content-Type: application/json" \
  -d '{"user_id": "usuario123", "plan": "pro"}'
```

Respuesta:
```json
{
  "success": true,
  "init_point": "https://www.mercadopago.com.co/checkout/xxx",
  "preference_id": "xxx"
}
```

El usuario hace click en `init_point` para pagar en MercadoPago.

## 7. Comisiones MercadoPago

MercadoPago cobra:
- **2.99% + $300 COP** por transferencia bancaria
- **3.49%** por tarjeta de crédito

Esto ya está descontado del dinero que recibes.

## 8. Recibir Dinero

MercadoPago deposita en tu cuenta bancaria cada día hábil (según tu banco).

---

## Alternativas si MercadoPago no funciona

- **PayPal**: https://paypal.com (genera facturas para Colombia)
- **Wompi**: https://www.wompi.co (pagos digitales locales)
- **PayU**: https://www.payulatam.com (Latinoamérica)
