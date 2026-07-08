# AI Resume Analyzer

An AI-powered tool to analyze resumes against job descriptions, extract skills, calculate match scores, and provide AI-powered improvement suggestions.

## Tech Stack
- **Backend:** Python, FastAPI
- **PDF Processing:** pdfplumber
- **DOCX Processing:** python-docx
- **Parsing:** Regex-based information extraction
- **AI:** Ollama (local LLM) / OpenRouter / OpenAI / Gemini / Claude — switchable via environment variable
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **Testing:** pytest
- **Deployment:** Render *(planned)*

## Progress Checklist
- [x] FastAPI project setup
- [x] File upload endpoint
- [x] PDF text extraction
- [x] Resume parsing (name, email, phone, LinkedIn, GitHub, sections)
- [x] Skill extraction (regex + set-based matching)
- [x] Skill synonym normalization (NLP = natural language processing, ML = machine learning)
- [x] JD matching algorithm (match %, missing/extra skills, category breakdown)
- [x] AI suggestions (multi-provider: Ollama, OpenRouter, OpenAI, Gemini, Claude)
- [x] Frontend UI (upload form, match score, AI suggestions display)
- [x] Multi-format file support (PDF, DOCX, TXT)
- [x] Multi-provider AI abstraction layer with factory pattern
- [ ] Dual mode — Applicant vs Recruiter
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
# Options: ollama | openrouter | openai | gemini | claude
AI_PROVIDER=ollama

# Ollama (local) — no API key needed, just run Ollama locally
# Pull a model first: ollama pull llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=llama3.2:3b

# OpenRouter — requires an API key from https://openrouter.ai
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODEL=meta-llama/llama-3.2-3b-instruct:free

# OpenAI — requires an API key from https://platform.openai.com
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini

# Gemini — requires an API key from https://aistudio.google.com
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.0-flash-lite

# Claude — requires an API key from https://console.anthropic.com
CLAUDE_API_KEY=your_key_here
CLAUDE_MODEL=claude-3-haiku-20240307
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

## Supported File Types

| Format | Extension | Notes |
|--------|-----------|-------|
| PDF | `.pdf` | Text-based PDFs only. Scanned/image PDFs are not supported. |
| Word Document | `.docx` | Full paragraph and table extraction. |
| Plain Text | `.txt` | UTF-8 and latin-1 encoding supported. |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serves frontend UI |
| GET | `/health` | Health check |
| GET | `/about` | Project info |
| POST | `/upload-resume` | Upload a resume file and save it |
| POST | `/extract-text` | Upload a file and extract raw cleaned text |
| POST | `/parse-resume` | Upload a file and get structured data (name, email, phone, LinkedIn, GitHub, sections) |
| POST | `/extract-skills` | Upload a file and get recognized skills from the resume |
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

---

## Future Improvements

### Recruiter Mode
The current tool is built for applicants. A recruiter mode is planned with a fundamentally different workflow:

- **Multi-resume upload** — upload multiple candidate resumes at once against a single job description
- **Candidate ranking** — automatically rank candidates by match percentage and skill coverage
- **Smart filtering** — filter candidates by notice period, current CTC, expected CTC, location, and experience level before ranking
- **Filter-aware ranking** — a candidate ranked #1 by skills may drop if they fail a filter (e.g. notice period too long), surfacing the next best fit automatically
- **Side-by-side comparison** — compare top candidates across skills, experience, and gaps in a single view
- **Bulk AI summaries** — one-paragraph AI assessment per candidate, optimized for quick recruiter review
- **Export** — download ranked candidate list as CSV or PDF

### Performance & Speed
- **Streaming AI responses** — stream tokens to the frontend as they generate instead of waiting for the full response, making the UI feel faster
- **Resume caching** — cache parsed resume data by file hash so re-uploading the same resume skips extraction and parsing
- **Async AI calls** — make the AI provider call non-blocking so the match result returns immediately while AI suggestions load separately
- **Prompt compression** — truncate resume and JD intelligently before sending to the model to reduce token count and inference time

### Accuracy & Intelligence
- **RAG for skills database** — replace the static `SKILLS_DB` dictionary with a vector database (FAISS or ChromaDB) so skill matching uses semantic similarity instead of exact string lookup. "Backend development" would then match "FastAPI" and "Django" contextually
- **Better prompt engineering** — few-shot prompting with verified examples to improve JSON adherence and reduce malformed responses across smaller models
- **Confidence scoring** — assign confidence levels to extracted skills based on context (listed in skills section vs mentioned in a project description vs implied)
- **Section-aware parsing** — distinguish between skills the candidate claims vs skills demonstrated in project descriptions vs skills mentioned in passing

### Infrastructure
- **Database integration** — store analysis results in PostgreSQL so users can retrieve past analyses without re-uploading
- **User authentication** — allow users to save their resume and track improvement over time across multiple job applications
- **REST API versioning** — version endpoints (`/v1/analyze-resume`) for backward compatibility as the API evolves
- **Rate limiting** — protect AI endpoints from abuse, especially when using paid cloud providers
- **Deployment to Render** — containerize with Docker and deploy with environment-based provider switching