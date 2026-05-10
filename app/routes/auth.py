from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.auth import api_key_manager

router = APIRouter()

class KeyRequest(BaseModel):
    user_id: str

class KeyResponse(BaseModel):
    success: bool
    api_key: str | None = None
    message: str

@router.post("/generate-key", response_model=KeyResponse)
async def generate_api_key(request: KeyRequest):
    try:
        key = api_key_manager.generate_key(request.user_id)
        return KeyResponse(
            success=True,
            api_key=key,
            message="API key generated. Save it securely!"
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
