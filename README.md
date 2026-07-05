# AI Resume Analyzer

An AI-powered tool to analyze resumes against job descriptions, extract skills, calculate match scores, and provide AI-powered improvement suggestions.

## Tech Stack
- **Backend:** Python, FastAPI
- **PDF Processing:** pdfplumber
- **Parsing:** Regex-based information extraction
- **AI:** Ollama (local LLM) / OpenRouter — switchable via environment variable
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Testing:** pytest
- **Deployment:** Render *(planned)*

## Progress Checklist
- [x] FastAPI project setup
- [x] File upload endpoint
- [x] PDF text extraction
- [x] Resume parsing (name, email, phone, LinkedIn, GitHub, sections)
- [x] Skill extraction (regex + set-based matching)
- [x] JD matching algorithm (match %, missing/extra skills, category breakdown)
- [x] AI suggestions (Ollama + OpenRouter with provider switching)
- [x] Frontend UI (upload form, match score, AI suggestions display)
- [ ] Multi-format file support (PDF, DOCX, TXT)
- [ ] Multi-provider AI (OpenAI, Gemini, Claude, OpenRouter, Ollama)
- [ ] Dual mode (Applicant vs Recruiter)
- [ ] Deployment

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/mohanv2005/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

Activate it:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example env file and fill in your values:
```bash
cp .env.example .env
```

```bash
# .env

# Which AI provider to use
AI_PROVIDER=ollama        # ollama | openrouter

# Ollama (local) — no API key needed, just run Ollama locally
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=llama3.2:3b

# OpenRouter — requires an API key from https://openrouter.ai
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODEL=meta-llama/llama-3.2-3b-instruct:free
```

Only the credentials for your active `AI_PROVIDER` are required.

---

## Usage

### Run the API Server
```bash
uvicorn app.main:app --reload
```

Then open your browser:
```
http://127.0.0.1:8000
```

For interactive API documentation:
```
http://127.0.0.1:8000/docs
```

### Run Tests
```bash
pytest -v
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serves frontend UI |
| GET | `/health` | Health check |
| GET | `/about` | Project info |
| POST | `/upload-resume` | Upload a resume PDF and save it |
| POST | `/extract-text` | Upload a PDF and extract raw cleaned text |
| POST | `/parse-resume` | Upload a PDF and get structured data (name, email, phone, LinkedIn, GitHub, sections) |
| POST | `/extract-skills` | Upload a PDF and get recognized skills from the resume |
| POST | `/match-resume` | Upload a resume + job description → skill match analysis |
| POST | `/analyze-resume` | Full pipeline: match analysis + AI-powered suggestions |

## Example Request

```bash
curl -X POST "http://127.0.0.1:8000/analyze-resume" \
     -F "file=@resume.pdf;type=application/pdf" \
     -F "job_description=We are looking for a Python developer with FastAPI experience..."
```

## Example Response

```json
{
  "filename": "resume.pdf",
  "match_percentage": 72.5,
  "matched_skills": ["python", "fastapi", "git", "sql"],
  "missing_skills": ["docker", "kubernetes"],
  "extra_skills": ["unity", "blender"],
  "missing_by_category": {
    "devops": ["docker", "kubernetes"]
  },
  "total_resume_skills": 12,
  "total_job_skills": 6,
  "total_matched": 4,
  "ai_suggestions": {
    "overall_assessment": "Strong Python candidate with relevant backend experience...",
    "match_quality": "strong",
    "missing_skills_advice": [
      {
        "skill": "docker",
        "priority": "critical",
        "advice": "Add Docker to your skills section and containerize one of your existing projects."
      }
    ],
    "resume_improvements": [
      "Add FastAPI explicitly to your Skills section"
    ],
    "ats_keywords": ["Docker", "REST API", "FastAPI"],
    "recommended_projects": [
      {
        "title": "Dockerized FastAPI Service",
        "description": "Containerize your existing Flask project using Docker.",
        "skills_covered": ["docker", "fastapi"]
      }
    ]
  },
  "ai_error": null,
  "message": "Analysis complete: 72.5% match"
}
```

## Future Improvements
- Multi-format file support (PDF, DOCX, TXT)
- Dual mode: Applicant (suggestions) vs Recruiter (ranking, pass/fail threshold)
- Multi-provider AI with native SDKs (OpenAI, Gemini, Claude)
- Deployment to Render