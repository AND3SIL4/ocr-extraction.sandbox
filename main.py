from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.files import router as files_router


app = FastAPI(
    title="PDF Processing API",
    description="API for uploading and downloading PDF files with unique IDs",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(files_router, prefix="/api/v1/files", tags=["files"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "PDF Processing API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
