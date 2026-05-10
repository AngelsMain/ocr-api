# OCR Document API - Guía de Uso

## 1. Generar API Key

```bash
curl -X POST http://localhost:8000/api/v1/auth/generate-key \
  -H "Content-Type: application/json" \
  -d '{"user_id": "usuario123"}'
```

Respuesta:
```json
{
  "success": true,
  "api_key": "xxxxxxxxxxxxxx",
  "message": "API key generated. Save it securely!"
}
```

## 2. Ver Planes y Precios

```bash
curl http://localhost:8000/api/v1/payments/plans
```

Planes disponibles:
- **Free**: $0/mes - 100 requests/mes
- **Pro**: $29/mes - 10,000 requests/mes
- **Enterprise**: $299/mes - Unlimited

## 3. Actualizar Plan (Stripe)

```bash
curl -X POST http://localhost:8000/api/v1/payments/upgrade-plan \
  -H "Content-Type: application/json" \
  -d '{"user_id": "usuario123", "plan": "pro"}'
```

## 4. Extraer Texto de un Documento

```bash
curl -X POST http://localhost:8000/api/v1/extract \
  -H "X-API-Key: TU_API_KEY" \
  -F "file=@documento.pdf"
```

Respuesta:
```json
{
  "success": true,
  "message": "Text extracted successfully",
  "data": {
    "filename": "documento.pdf",
    "file_type": "pdf",
    "extracted_text": "Texto extraído...",
    "confidence_score": 0.85,
    "file_size": 102400,
    "processing_time": 1.23,
    "created_at": "2026-05-10T12:30:45"
  }
}
```

## Formatos Soportados
- PDF
- JPG / JPEG
- PNG

## Límites
- Tamaño máximo: 10MB por archivo
- Free: 100 requests/mes
- Pro: 10,000 requests/mes
