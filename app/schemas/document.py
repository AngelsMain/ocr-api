from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DocumentBase(BaseModel):
    filename: str
    file_type: str

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    extracted_text: Optional[str]
    confidence_score: Optional[float]
    file_size: int
    processing_time: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True

class OCRResponse(BaseModel):
    success: bool
    message: str
    data: Optional[DocumentResponse] = None
    error: Optional[str] = None
