# PDF Processing API

A FastAPI-based API for uploading and downloading PDF files with unique ID management.

## Features

- **Upload PDF files**: Upload PDF documents and get a unique ID
- **Download PDF files**: Retrieve PDF files by their unique ID
- **File validation**: Ensures only valid PDF files are accepted
- **Secure file handling**: Files are renamed and stored securely
- **Layered architecture**: Clean separation of concerns with routes, services, models, and utilities

## Installation

1. Install dependencies:
```bash
uv sync
```

2. Run the application:
```bash
uv run uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Upload PDF File
- **POST** `/api/v1/files/upload`
- Upload a PDF file and receive a unique file ID
- **Request**: Multipart form data with PDF file
- **Response**: JSON with file information

### Download PDF File
- **GET** `/api/v1/files/download/{file_id}`
- Download a PDF file by its unique ID
- **Response**: PDF file download

### Get File Information
- **GET** `/api/v1/files/info/{file_id}`
- Get information about a PDF file by ID
- **Response**: JSON with file metadata

## Project Structure

```
app/
├── routes/          # API endpoints
├── services/        # Business logic
├── models/          # Pydantic models
└── utils/           # Utility functions
```

## Development

- Install dependencies: `uv sync`
- Run application: `uv run fastapi dev`
- Format code: `uv run python -m black .` (when black is added)
- Lint code: `uv run python -m flake8` (when flake8 is added)