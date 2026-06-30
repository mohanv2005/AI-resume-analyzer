# AI Resume Analyzer

An AI-powered tool to analyze resumes against job descriptions, extract skills, calculate match scores, and provide improvement suggestions.

## Tech Stack
- **Backend:** Python, FastAPI
- **PDF Processing:** pdfplumber
- **Parsing:** Regex-based information extraction
- **AI:** Google Gemini / OpenAI *(planned)*
- **Frontend:** HTML, CSS, Bootstrap, JavaScript *(planned)*
- **Deployment:** Render *(planned)*
- **Testing:** pytest

## Progress Checklist
- [x] FastAPI project setup
- [x] File upload endpoint
- [x] PDF text extraction
- [x] Resume parsing (name, email, phone, LinkedIn, GitHub, sections)
- [x] Skill extraction (regex + set-based matching)
- [ ] JD matching algorithm
- [ ] AI suggestions
- [ ] Frontend UI
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

---

## Usage

### Run the API Server
```bash
uvicorn app.main:app --reload
```

Then open browser:
```plaintext
http://127.0.0.1:8000/docs
```

This opens the interactive Swagger UI where you can test every endpoint directly — upload a resume PDF and see the parsed output without writing any client code.

### Run Tests
```bash
pytest -v
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root info |
| GET | `/health` | Health check |
| GET | `/about` | Project info |
| POST | `/upload-resume` | Upload a resume PDF and save it |
| POST | `/extract-text` | Upload a PDF and extract raw cleaned text |
| POST | `/parse-resume` | Upload a PDF and get structured data (name, email, phone, LinkedIn, GitHub, sections) |
| POST | `/extract-skills` | Upload a PDF and get recognized skills from the resume |

## Example Request

```bash
curl -X POST "http://127.0.0.1:8000/parse-resume" \
     -F "file=@resume.pdf;type=application/pdf"
```

## Example Response

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+91 9876543210",
  "linkedin": "https://www.linkedin.com/in/johndoe/",
  "github": "https://github.com/johndoe",
  "skills_section": "Languages: Python, JavaScript\nTools: Git, Docker",
  "experience_section": "",
  "education_section": "B.Tech in Computer Science",
  "raw_text": "...",
  "message": "Resume parsed successfully"
}
```
