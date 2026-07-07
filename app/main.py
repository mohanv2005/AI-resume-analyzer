import os

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.ai import get_ai_suggestions
from app.models import (
    UploadResponse, ErrorResponse, ExtractResponse,
    ParsedResume, SkillExtractionResponse, MatchResponse,
    FullAnalysisResponse, AIsuggestions
)
from app.parser import extract_text_from_pdf, get_text_stats, parse_resume
from app.matcher import extract_skills_from_text, extract_skills_from_section, calculate_match



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

app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_DIR = "uploads"
ALLOWED_CONTENT_TYPES = ["application/pdf"]
MAX_FILE_SIZE = 5 * 1024 * 1024

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "AI Resume Analyzer is running"
    }

@app.get("/", response_class=FileResponse)
def root():
    return FileResponse("static/index.html")

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
    
    


    parsed = parse_resume(extraction["text"], file_path=save_path)
    parsed["message"] = "Resume parsed successfully"

    return ParsedResume(
        name=parsed.get("name"),
        email=parsed.get("email"),
        phone=parsed.get("phone"),
        linkedin=parsed.get("linkedin"),
        github=parsed.get("github"),
        skills_section=parsed.get("skills_section", ""),
        experience_section=parsed.get("experience_section", ""),
        education_section=parsed.get("education_section", ""),
        raw_text=parsed.get("raw_text", ""),
        message="Resume parsed successfully"
    )

@app.post("/extract-skills", response_model=SkillExtractionResponse)
async def extract_skills_endpoint(file: UploadFile = File(...)):
    """
    Full pipeline: upload PDF → extract text → parse → extract skills.
    Returns all recognized skills found in the resume.
    """

    # Validate
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Only PDF files accepted.")

    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="File is empty.")
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File exceeds 5MB limit.")

    # Save
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as buffer:
        buffer.write(content)

    # Extract text
    extraction = extract_text_from_pdf(save_path)
    if not extraction["success"]:
        raise HTTPException(status_code=400, detail=extraction["error"])

    # Parse to get skills section
    parsed = parse_resume(extraction["text"])

    # Extract skills two ways:
    # 1. Scan the full resume text (catches skills mentioned in projects)
    skills_full = extract_skills_from_text(extraction["text"])

    # 2. Scan only the skills section (more precise)
    skills_section = extract_skills_from_section(parsed.get("skills_section", ""))

    return SkillExtractionResponse(
        filename=file.filename,
        skills_found=skills_full,
        skills_from_section=skills_section,
        total_skills=len(skills_full),
        message=f"Found {len(skills_full)} skills in resume"
    )

@app.post("/match-resume", response_model=MatchResponse)
async def match_resume_endpoint(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
     """
    Full pipeline: upload resume PDF + job description text → match analysis.
    Returns match percentage, matched/missing/extra skills, and category breakdown.
    """
     if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Only PDF files accepted.")
     
     content = await file.read()
     if len(content) == 0:
        raise HTTPException(status_code=400, detail="File is empty.")   
     if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File exceeds 5MB limit.")
     
     if len(job_description) < 20:
         raise HTTPException(status_code=400, detail="Job description is too short. Please provide a more detailed description.")
     
     os.makedirs(UPLOAD_DIR, exist_ok=True)
     save_path = os.path.join(UPLOAD_DIR, file.filename)
     with open(save_path, "wb") as buffer:
        buffer.write(content)

     extraction = extract_text_from_pdf(save_path)
     if not extraction["success"]:
        raise HTTPException(status_code=400, detail=extraction["error"])
     
     parsed = parse_resume(extraction["text"], file_path=save_path)

     resume_skills = extract_skills_from_text(extraction["text"])

     job_skills = extract_skills_from_text(job_description)

     match_result = calculate_match(resume_skills, job_skills)

     return MatchResponse(
        filename=file.filename,
        match_percentage=match_result["match_percentage"],
        matched_skills=match_result["matched_skills"],
        missing_skills=match_result["missing_skills"],
        extra_skills=match_result["extra_skills"],
        missing_by_category=match_result["missing_by_category"],
        total_resume_skills=match_result["total_resume_skills"],
        total_job_skills=match_result["total_job_skills"],
        total_matched=match_result["total_matched"],
        message=f"Match analysis complete: {match_result['match_percentage']}% match"
    )



@app.post("/analyze-resume", response_model=FullAnalysisResponse)
async def analyze_resume_endpoint(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Flagship endpoint: upload resume PDF + job description →
    skill match + AI-powered suggestions.
    """

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Only PDF files accepted.")

    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="File is empty.")
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File exceeds 5MB limit.")

    if len(job_description.strip()) < 20:
        raise HTTPException(
            status_code=400,
            detail="Job description too short. Please provide a complete JD."
        )

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as buffer:
        buffer.write(content)

    extraction = extract_text_from_pdf(save_path)
    if not extraction["success"]:
        raise HTTPException(status_code=400, detail=extraction["error"])

    parsed = parse_resume(extraction["text"], file_path=save_path)

    resume_skills = extract_skills_from_text(extraction["text"])
    job_skills = extract_skills_from_text(job_description)
    match_result = calculate_match(resume_skills, job_skills)

    # AI call is isolated — failure here doesn't crash the endpoint
    ai_result = get_ai_suggestions(
        resume_text=extraction["text"],
        job_description=job_description,
        match_result=match_result
    )

    ai_suggestions = None
    ai_error = None

    if ai_result["success"]:
        try:
            raw_suggestions = ai_result["suggestions"]

            # Normalize resume_improvements — flatten dicts to strings if model misbehaved
            if "resume_improvements" in raw_suggestions:
                normalized = []
                for item in raw_suggestions["resume_improvements"]:
                    if isinstance(item, str):
                        normalized.append(item)
                    elif isinstance(item, dict):
                        normalized.append(" ".join(str(v) for v in item.values()))
                raw_suggestions["resume_improvements"] = normalized

            # Same normalization for ats_keywords just in case
            if "ats_keywords" in raw_suggestions:
                normalized = []
                for item in raw_suggestions["ats_keywords"]:
                    if isinstance(item, str):
                        normalized.append(item)
                    elif isinstance(item, dict):
                        normalized.append(" ".join(str(v) for v in item.values()))
                raw_suggestions["ats_keywords"] = normalized

            ai_suggestions = AIsuggestions(**raw_suggestions)
        except Exception as e:
            ai_error = f"AI response structure error: {str(e)}"
    else:
        ai_error = ai_result["error"]

    return FullAnalysisResponse(
        filename=file.filename,
        match_percentage=match_result["match_percentage"],
        matched_skills=match_result["matched_skills"],
        missing_skills=match_result["missing_skills"],
        extra_skills=match_result["extra_skills"],
        missing_by_category=match_result["missing_by_category"],
        total_resume_skills=match_result["total_resume_skills"],
        total_job_skills=match_result["total_job_skills"],
        total_matched=match_result["total_matched"],
        ai_suggestions=ai_suggestions,
        ai_error=ai_error,
        message=f"Analysis complete: {match_result['match_percentage']}% match"
    )



