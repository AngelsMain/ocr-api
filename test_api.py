#!/usr/bin/env python
import requests
import json

BASE_URL = "http://localhost:8000"
API_KEY = None

def test_health():
    """Test health endpoint"""
    print("\n[1] Probando /health...")
    resp = requests.get(f"{BASE_URL}/health")
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.json()}")

def test_generate_key():
    """Generate API key"""
    global API_KEY
    print("\n[2] Generando API key...")
    resp = requests.post(
        f"{BASE_URL}/api/v1/auth/generate-key",
        json={"user_id": "test_user"}
    )
    print(f"Status: {resp.status_code}")
    data = resp.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    if data.get("api_key"):
        API_KEY = data["api_key"]
        print(f"\nAPI Key guardada: {API_KEY[:20]}...")

def test_get_plans():
    """Get available plans"""
    print("\n[3] Obteniendo planes disponibles...")
    resp = requests.get(f"{BASE_URL}/api/v1/payments/plans")
    print(f"Status: {resp.status_code}")
    print(f"Response: {json.dumps(resp.json(), indent=2)}")

def test_extract_no_key():
    """Test extract without API key"""
    print("\n[4] Intentando extraer sin API key...")
    with open("test_image.jpg", "rb") as f:
        files = {"file": f}
        resp = requests.post(f"{BASE_URL}/api/v1/extract", files=files)
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.json()}")

if __name__ == "__main__":
    print("=== OCR API Test Suite ===")
    print(f"Base URL: {BASE_URL}")
    
    try:
        test_health()
        test_generate_key()
        test_get_plans()
        test_extract_no_key()
        
        print("\n=== Pruebas completadas ===")
        if API_KEY:
            print(f"\nPara extraer texto, usa:")
            print(f"curl -X POST {BASE_URL}/api/v1/extract \\")
            print(f"  -H 'X-API-Key: {API_KEY}' \\")
            print(f"  -F 'file=@documento.pdf'")
    except requests.exceptions.ConnectionError:
        print("\nError: No se puede conectar a la API.")
        print("Asegúrate de que el servidor esté corriendo: python -m uvicorn app.main:app")
