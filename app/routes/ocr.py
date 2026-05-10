from fastapi import APIRouter, UploadFile, File, HTTPException, Header
from pydantic import BaseModel
from app.services.ocr_service import ocr_service
from app.config import settings
from app.auth import api_key_manager
from datetime import datetime

router = APIRouter()

class OCRResponse(BaseModel):
    success: bool
    message: str
    data: dict | None = None
    error: str | None = None

@router.post("/extract", response_model=OCRResponse)
async def extract_text(
    file: UploadFile = File(...),
    x_api_key: str = Header(None)
):
    try:
        # Validate API key
        if not x_api_key:
            raise HTTPException(status_code=401, detail="API key required")

        key_data = api_key_manager.verify_key(x_api_key)
        if not key_data:
            raise HTTPException(status_code=401, detail="Invalid API key")

        # Check rate limit
        if not api_key_manager.check_rate_limit(x_api_key):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

        # Validate file size
        contents = await file.read()
        if len(contents) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: {settings.MAX_FILE_SIZE / 1024 / 1024}MB"
            )

        # Validate file type
        file_ext = file.filename.split(".")[-1].lower()
        if file_ext not in settings.ALLOWED_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file format. Allowed: {settings.ALLOWED_FORMATS}"
            )

        # Process document
        text, confidence, processing_time = ocr_service.process_document(
            contents,
            file_ext
        )

        # Increment usage
        api_key_manager.increment_usage(x_api_key)

        return OCRResponse(
            success=True,
            message="Text extracted successfully",
            data={
                "filename": file.filename,
                "file_type": file_ext,
                "extracted_text": text,
                "confidence_score": confidence,
                "file_size": len(contents),
                "processing_time": processing_time,
                "created_at": datetime.now().isoformat()
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        return OCRResponse(
            success=False,
            message="Error processing document",
            error=str(e)
        )

