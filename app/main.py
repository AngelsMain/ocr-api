from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import ocr, auth, payments

app = FastAPI(
    title="OCR Document API",
    description="API para extraer texto de documentos usando OCR",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(ocr.router, prefix="/api/v1", tags=["OCR"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["Payments"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
def root():
    return {"message": "OCR Document API - Use /docs for documentation"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
