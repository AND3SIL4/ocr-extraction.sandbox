from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

from app.services.file_service import FileService
from app.models.file_models import FileInfo, FileUploadResponse

router = APIRouter()
file_service = FileService()


@router.post(
    "/upload",
    response_model=FileUploadResponse,
    summary="Upload PDF file",
    description="Upload a PDF file, rename it with a unique ID, and move it to processed folder"
)
async def upload_pdf_file(file: UploadFile = File(...)) -> FileUploadResponse:
    """
    Upload a PDF file.

    - **file**: PDF file to upload
    - Returns file upload information including unique ID
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed"
            )

        # Read file content
        file_content = await file.read()

        # Validate file size (max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if len(file_content) > max_size:
            raise HTTPException(
                status_code=400,
                detail="File size exceeds maximum limit of 10MB"
            )

        # Process file upload
        result = file_service.upload_pdf_file(file_content, file.filename)

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get(
    "/download/{file_id}",
    summary="Download PDF file",
    description="Download a PDF file by its unique ID"
)
async def download_pdf_file(file_id: str):
    """
    Download a PDF file by ID.

    - **file_id**: Unique identifier of the PDF file
    - Returns the PDF file for download
    """
    try:
        # Get file information
        file_info = file_service.get_pdf_file(file_id)

        if not file_info:
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )

        # Get file content
        file_content = file_service.get_file_content(file_id)

        if not file_content:
            raise HTTPException(
                status_code=404,
                detail="File content could not be retrieved"
            )

        # Return file as download
        return FileResponse(
            path=file_info.file_path,
            media_type='application/pdf',
            filename=f"{file_id}.pdf"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get(
    "/info/{file_id}",
    summary="Get PDF file information",
    description="Get information about a PDF file by its unique ID"
)
async def get_pdf_file_info(file_id: str) -> FileInfo:
    """
    Get PDF file information by ID.

    - **file_id**: Unique identifier of the PDF file
    - Returns file information
    """
    try:
        file_info = file_service.get_pdf_file(file_id)

        if not file_info:
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )

        return file_info

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")