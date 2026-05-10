# 📄 OCR Document API

API para extraer texto de documentos **(PDF, JPG, PNG)** usando OCR con Tesseract.

**Características:**
- ✅ Extracción de texto con OCR (español + inglés)
- ✅ Pagos con PayPal
- ✅ Autenticación con API Keys
- ✅ Rate limiting por plan
- ✅ Docker ready

---

## 🚀 Inicio rápido con Docker

### 1. Requisitos

- **Docker Desktop** instalado: https://www.docker.com/products/docker-desktop
- **PayPal Developer** credenciales (ver `PAYPAL_GUIDE.md`)

### 2. Clonar/Descargar proyecto

```bash
cd tu-carpeta-proyecto
```

### 3. Configurar `.env`

Copia `.env.example` → `.env` y rellena:

```env
PAYPAL_CLIENT_ID=tu_client_id
PAYPAL_CLIENT_SECRET=tu_secret
PAYPAL_MODE=sandbox
```

Ver `PAYPAL_GUIDE.md` para obtener credenciales.

### 4. Correr con Docker

```bash
docker-compose up --build
```

La API estará en: **http://localhost:8000**

Documentación interactiva: **http://localhost:8000/docs**

---

## 📚 Documentación

- **`PAYPAL_GUIDE.md`** - Guía completa de PayPal
- **`API_USAGE.md`** - Cómo usar cada endpoint
- **`DEPLOYMENT.md`** - Desplegar en Render

---

## 🧪 Endpoints principales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/health` | GET | Verifica que API está viva |
| `/api/v1/auth/generate-key` | POST | Genera API key |
| `/api/v1/extract` | POST | Extrae texto de documento |
| `/api/v1/payments/plans` | GET | Ver planes y precios |
| `/api/v1/payments/create-payment` | POST | Crear pago PayPal |

---

## 💵 Monetización

Tu API cobra por planes:

- **Free**: $0 - 100 requests/mes
- **Pro**: $29 USD - 10,000 requests/mes
- **Enterprise**: $299 USD - Ilimitado

Los usuarios pagan con **PayPal** → dinero llega a tu cuenta bancaria colombiana.

Ver `PAYPAL_GUIDE.md` para detalles.

---

## 🔧 Desarrolladores

### Instalar localmente (sin Docker)

```bash
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### Stack

- **FastAPI** - Framework web
- **Tesseract OCR** - Extracción de texto
- **PayPal SDK** - Pagos
- **Docker** - Containerización

---

## 📞 Soporte

¿Preguntas sobre PayPal? Ver `PAYPAL_GUIDE.md`

¿Errores de OCR? Los acentos se corrigen automáticamente, pero reporta si encuentras fallos.

---

## 📄 Licencia

MIT - Usa libremente para proyectos comerciales.
