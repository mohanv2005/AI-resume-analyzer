import os

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models import UploadResponse, ErrorResponse, ExtractResponse, ParsedResume
from app.parser import extract_text_from_pdf, get_text_stats, parse_resume


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
MAX_FILE_SIZE = 5 * 1024 * 1024

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
        "page": "About",
        "project": "AI Resume Analyzer",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.post("/upload-resume", response_model=UploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: '{file.content_type}'. Only PDF files are accepted."
        )

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

@app.post("/extract-text", response_model=ExtractResponse)
async def extract_text(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{file.content_type}'. Only PDFs accepted."
        )

    content = await file.read()
    file_size = len(content)

    if file_size == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size {file_size} bytes exceeds 5MB limit."
        )

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    save_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(save_path, "wb") as buffer:
            buffer.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Could not save file: {str(e)}"
        )

    result = extract_text_from_pdf(save_path)

    if not result["success"]:
        raise HTTPException(
            status_code=400,
            detail=result["error"]
        )

    stats = get_text_stats(result["text"])

    return ExtractResponse(
        filename=file.filename,
        page_count=result["page_count"],
        word_count=stats["word_count"],
        line_count=stats["line_count"],
        char_count=stats["char_count"],
        extracted_text=result["text"],
        message="Text extracted successfully"
    )


@app.post("/parse-resume", response_model=ParsedResume)
async def parse_resume_endpoint(file: UploadFile = File(...)):
    """
    Full pipeline: upload PDF → extract text → parse structured data.
    Returns name, email, phone, LinkedIn, GitHub, and key sections.
    """

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Only PDF files accepted.")

    content = await file.read()

    if len(content) == 0:
        raise HTTPException(status_code=400, detail="File is empty.")
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File exceeds 5MB limit.")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as buffer:
        buffer.write(content)

    extraction = extract_text_from_pdf(save_path)
    if not extraction["success"]:
        raise HTTPException(status_code=400, detail=extraction["error"])

    parsed = parse_resume(extraction["text"])
    parsed["message"] = "Resume parsed successfully"

    return parsed