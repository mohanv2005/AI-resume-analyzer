import os
import shutil

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import UploadResponse, ErrorResponse

app = FastAPI(
    title="AI Resume Analyzer",         
    description="Upload a resume PDF and match it against a job description using AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
ALLOWED_CONTENT_TYPES = ["application/pdf"]
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

@app.get("/health")
def health_check():
    return {
            "status": "healthy",
             "message": "AI Resume Analyzer is running"
      }

@app.get("/")
def root():
    return {
        "project": "AI Resume Analyzer",
        "version": "1.0.0",
        "docs": "/docs"    
    }

@app.get("/about")
def about():
    return {
        "page" : "About",
        "project": "AI Resume Analyzer",
        "version": "1.0.0",
        "docs": "/docs"    
    }

@app.post("/upload-resume", response_model=UploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid file type: '{file.content_type}'. Only PDF files are accepted.")

    content = await file.read()

    file_size = len(content)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large: {file_size} bytes. Maximum allowed is {MAX_FILE_SIZE} bytes (5MB)."
        )

    if file_size == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    save_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(save_path, "wb") as buffer: 
            buffer.write(content)   
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save the file: {str(e)}"
        )
    
    return UploadResponse(
        filename=file.filename,
        file_size=file_size,
        content_type=file.content_type,
        message="Resume uploaded successfully.",
        saved_path=save_path
    )