from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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