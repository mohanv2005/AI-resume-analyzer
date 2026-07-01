from pydantic import BaseModel
from typing import Optional

class UploadResponse(BaseModel):
    filename: str           
    file_size: int          
    content_type: str       
    message: str            
    saved_path: str        


class ErrorResponse(BaseModel):
    error: str              
    detail: str             

class ExtractResponse(BaseModel):
    filename: str
    page_count: int
    word_count: int
    line_count: int
    char_count: int
    extracted_text: str         
    message: str

class ParsedResume(BaseModel):
    name: Optional[str] = None         
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    skills_section: str = ""           
    experience_section: str = ""
    education_section: str = ""
    raw_text: str = ""
    message: str = ""

class SkillExtractionResponse(BaseModel):
    filename: str
    skills_found: list[str]          
    skills_from_section: list[str]   
    total_skills: int
    message: str

class MatchResponse(BaseModel):
    filename: str
    match_percentage: float
    matched_skills: list[str]
    missing_skills: list[str]
    extra_skills: list[str]
    missing_by_category: dict[str, list[str]]
    total_resume_skills: int
    total_job_skills: int
    total_matched: int
    message: str

class MissingSkillAdvice(BaseModel):
    skill: str
    priority: str
    advice: str


class RecommendedProject(BaseModel):
    title: str
    description: str
    skills_covered: list[str]

class AIsuggestions(BaseModel):
    overall_assessment: str
    match_quality: str
    missing_skills_advice: list[MissingSkillAdvice]
    resume_improvements: list[str]
    ats_keywords: list[str]
    recommended_projects: list[RecommendedProject]

class FullAnalysisResponse(BaseModel):
    filename: str
    match_percentage: float
    matched_skills: list[str]
    missing_skills: list[str]
    extra_skills: list[str]
    missing_by_category: dict[str, list[str]]
    total_resume_skills: int
    total_job_skills: int
    total_matched: int
    ai_suggestions: Optional[AIsuggestions] = None
    ai_error: Optional[str] = None
    message: str