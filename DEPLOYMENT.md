# Despliegue en Render

## Opción 1: Despliegue Automático (Recomendado)

### Paso 1: Preparar el repositorio
```bash
git init
git add .
git commit -m "Initial commit: OCR Document API"
git remote add origin https://github.com/tu-usuario/ocr-api.git
git push -u origin main
```

### Paso 2: Conectar a Render
1. Ir a https://render.com
2. Crear cuenta / Iniciar sesión
3. Click en "New +" → "Web Service"
4. Conectar repositorio de GitHub
5. Seleccionar tu repositorio `ocr-api`

### Paso 3: Configurar el servicio
- **Name**: `ocr-api`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Paso 4: Variables de entorno
Agregar en Render dashboard:
```
SECRET_KEY=ocr-api-secret-key-2026
STRIPE_SECRET_KEY=sk_test_xxxxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxx
TESSERACT_PATH=/usr/bin/tesseract
```

### Paso 5: Deploy
- Click en "Deploy"
- Esperar 5-10 minutos
- Tu API estará disponible en: `https://ocr-api-xxxxx.onrender.com`

---

## Opción 2: Docker (Alternativa)

### Con Render
1. Construir imagen: `docker build -t ocr-api .`
2. Subir a Docker Hub
3. En Render, seleccionar "Docker" y proporcionar la imagen

### Con Railway/Heroku
- Railway (más barato): https://railway.app
- Heroku (requiere tarjeta): https://heroku.com

---

## Monetización - Pasos Siguientes

1. **Integrar pagos reales con Stripe**
   - Usar claves secretas de producción (no test)
   - Implementar webhooks para confirmar pagos
   
2. **Agregar base de datos**
   - PostgreSQL en Render (gratis)
   - Guardar usuarios y su uso de API
   
3. **Marketing**
   - Product Hunt
   - Dev.to
   - Comunidades dev

---

## URLs de Prueba (local)

- **Documentación**: http://localhost:8000/docs
- **Generar API Key**: 
  ```bash
  curl -X POST http://localhost:8000/api/v1/auth/generate-key \
    -H "Content-Type: application/json" \
    -d '{"user_id": "test"}'
  ```

- **Extraer texto**:
  ```bash
  curl -X POST http://localhost:8000/api/v1/extract \
    -H "X-API-Key: YOUR_KEY" \
    -F "file=@test.pdf"
  ```
