import shutil
from pathlib import Path
from typing import Optional
from datetime import datetime

from app.models.file_models import FileUploadResponse, FileInfo
from app.utils.file_utils import (
    generate_file_id,
    ensure_directory_exists,
    is_pdf_file,
    get_file_size,
    sanitize_filename,
    get_upload_directory,
    get_processed_directory
)


class FileService:
    """Service class for handling file operations."""

    def __init__(self):
        self.upload_dir = get_upload_directory()
        self.processed_dir = get_processed_directory()
        ensure_directory_exists(self.upload_dir)
        ensure_directory_exists(self.processed_dir)

    def upload_pdf_file(self, file_content: bytes, original_filename: str) -> FileUploadResponse:
        """
        Upload a PDF file, rename it with a unique ID, and move it to processed folder.

        Args:
            file_content: The file content as bytes
            original_filename: Original filename from upload

        Returns:
            FileUploadResponse with upload details

        Raises:
            ValueError: If file is not a valid PDF or other validation fails
        """
        # Sanitize filename
        safe_filename = sanitize_filename(original_filename)

        # Generate unique file ID
        file_id = generate_file_id()

        # Create temporary file path in uploads directory
        temp_filename = f"{file_id}_temp.pdf"
        temp_file_path = Path(self.upload_dir) / temp_filename

        try:
            # Save file temporarily
            with open(temp_file_path, 'wb') as f:
                f.write(file_content)

            # Validate it's a PDF
            if not is_pdf_file(str(temp_file_path)):
                temp_file_path.unlink()  # Delete invalid file
                raise ValueError("Uploaded file is not a valid PDF")

            # Create final filename and path in processed directory
            final_filename = f"{file_id}.pdf"
            final_file_path = Path(self.processed_dir) / final_filename

            # Move file to processed directory
            shutil.move(str(temp_file_path), str(final_file_path))

            # Get file size
            file_size = get_file_size(str(final_file_path))

            return FileUploadResponse(
                file_id=file_id,
                original_filename=safe_filename,
                stored_filename=final_filename,
                file_size=file_size,
                upload_time=datetime.now(),
                message="File uploaded and processed successfully"
            )

        except Exception as e:
            # Clean up temporary file if it exists
            if temp_file_path.exists():
                temp_file_path.unlink()
            raise ValueError(f"Failed to upload file: {str(e)}")

    def get_pdf_file(self, file_id: str) -> Optional[FileInfo]:
        """
        Get PDF file information by ID.

        Args:
            file_id: The unique file ID

        Returns:
            FileInfo if file exists, None otherwise
        """
        # Sanitize file_id to prevent path traversal
        safe_file_id = sanitize_filename(file_id)

        # Construct file path
        filename = f"{safe_file_id}.pdf"
        file_path = Path(self.processed_dir) / filename

        if not file_path.exists():
            return None

        # Verify it's actually a PDF
        if not is_pdf_file(str(file_path)):
            return None

        file_size = get_file_size(str(file_path))

        return FileInfo(
            file_id=safe_file_id,
            original_filename="",  # We don't store original filename for downloads
            stored_filename=filename,
            file_size=file_size,
            upload_time=datetime.fromtimestamp(file_path.stat().st_ctime),
            file_path=str(file_path)
        )

    def get_file_content(self, file_id: str) -> Optional[bytes]:
        """
        Get PDF file content by ID.

        Args:
            file_id: The unique file ID

        Returns:
            File content as bytes if file exists, None otherwise
        """
        file_info = self.get_pdf_file(file_id)
        if not file_info:
            return None

        try:
            with open(file_info.file_path, 'rb') as f:
                return f.read()
        except Exception:
            return None