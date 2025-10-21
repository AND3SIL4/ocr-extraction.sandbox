from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FileUploadResponse(BaseModel):
    """Response model for file upload operations."""
    file_id: str
    original_filename: str
    stored_filename: str
    file_size: int
    upload_time: datetime
    message: str


class FileDownloadRequest(BaseModel):
    """Request model for file download operations."""
    file_id: str


class FileInfo(BaseModel):
    """Model containing file information."""
    file_id: str
    original_filename: str
    stored_filename: str
    file_size: int
    upload_time: datetime
    file_path: str


class ErrorResponse(BaseModel):
    """Standard error response model."""
    error: str
    message: str
    details: Optional[str] = None