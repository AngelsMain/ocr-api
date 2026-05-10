from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.sql import func
from app.database import Base

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(10), nullable=False)
    extracted_text = Column(Text, nullable=True)
    confidence_score = Column(Float, nullable=True)
    file_size = Column(Integer, nullable=False)
    processing_time = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
