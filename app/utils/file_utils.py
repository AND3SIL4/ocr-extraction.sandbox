import os
import uuid
from pathlib import Path
from typing import Optional
from datetime import datetime


def generate_file_id() -> str:
    """Generate a unique file ID."""
    return str(uuid.uuid4())


def ensure_directory_exists(directory_path: str) -> None:
    """Create directory if it doesn't exist."""
    Path(directory_path).mkdir(parents=True, exist_ok=True)


def is_pdf_file(file_path: str) -> bool:
    """Check if a file is a valid PDF by checking file extension and PDF header."""
    try:
        # Check file extension
        if not file_path.lower().endswith('.pdf'):
            return False

        # Check PDF header
        with open(file_path, 'rb') as f:
            header = f.read(8)
            return header.startswith(b'%PDF-')
    except Exception:
        return False


def get_file_size(file_path: str) -> int:
    """Get file size in bytes."""
    return os.path.getsize(file_path)


def get_file_info(file_path: str) -> Optional[dict]:
    """Get file information."""
    if not os.path.exists(file_path):
        return None

    stat = os.stat(file_path)
    return {
        'size': stat.st_size,
        'created_time': datetime.fromtimestamp(stat.st_ctime),
        'modified_time': datetime.fromtimestamp(stat.st_mtime)
    }


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent path traversal attacks."""
    return os.path.basename(filename)


def get_upload_directory() -> str:
    """Get the upload directory path."""
    return "uploads"


def get_processed_directory() -> str:
    """Get the processed files directory path."""
    return "processed"