import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  

def get_gemini_client():
  """
  Configures and returns the Gemini client.
    Separated into its own function so the configuration is testable
    and can be swapped out easily (e.g., for a different AI provider).

    Returns:
        Configured GenerativeModel instance

    Raises:
        ValueError: if GEMINI_API_KEY is not set in environment
  """
  base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
  
  # Ollama runs locally — no API key needed
  # base_url points to local Ollama server
  # api_key="ollama" is a placeholder (Ollama ignores it but OpenAI client requires it)
  client = OpenAI(
      base_url=base_url,
      api_key="ollama"
  )

  return client

def build_prompt(
    resume_text: str,
    job_description: str,
    match_result: dict
) -> str:
    """
    Building the prompt we send to Gemini.
    adds resume content, JD, and match data so AI has full context.

    Args:
        resume_text: Raw extracted resume text
        job_description: The job description the user provided
        match_result: Output from calculate_match()

    Returns:
        Formatted prompt string
    """
    
    # Formating the match data cleanly for the prompt
    match_summary = f"""
      Match Percentage: {match_result['match_percentage']}%
      Matched Skills: {', '.join(match_result['matched_skills']) or 'None'}
      Missing Skills: {', '.join(match_result['missing_skills']) or 'None'}
      Missing by Category: {json.dumps(match_result['missing_by_category'], indent=2)}
      Extra Skills (candidate has, JD doesn't mention): {', '.join(match_result['extra_skills']) or 'None'}
      """
    
    prompt = f"""
You are an expert resume coach and ATS (Applicant Tracking System) optimization specialist 
with 10 years of experience helping software engineers land jobs at top tech companies.

You have been given the following information about a job application:

---RESUME---
{resume_text}

---JOB DESCRIPTION---
{job_description}

---SKILL MATCH ANALYSIS---
{match_summary}

---YOUR TASK---
Analyze the resume against the job description and provide specific, actionable suggestions.

IMPORTANT RULES:
- Be specific. Reference actual content from the resume.
- Do not give generic advice like "improve your skills". 
- Every suggestion must be actionable (the candidate must know exactly what to change).
- For missing skills, assess whether they are CRITICAL (must have) or NICE TO HAVE.
- Consider that skill matching is keyword-based and may miss contextual matches.

Respond ONLY with a valid JSON object in this exact format (no markdown, no backticks, 
no explanation outside the JSON):

{{
  "overall_assessment": "2-3 sentence summary of fit for this role",
  "match_quality": "strong" | "moderate" | "weak",
  "missing_skills_advice": [
    {{
      "skill": "skill name",
      "priority": "critical" | "nice_to_have",
      "advice": "specific actionable advice"
    }}
  ],
  "resume_improvements": [
    "specific improvement with exact wording suggestions"
  ],
  "ats_keywords": [
    "keyword to add to resume"
  ],
  "recommended_projects": [
    {{
      "title": "project name",
      "description": "what to build and why it addresses the gap",
      "skills_covered": ["skill1", "skill2"]
    }}
  ]
}}
"""
    return prompt

def get_ai_suggestions(
    resume_text: str,
    job_description: str,
    match_result: dict
) -> str:
    """
     Main function that calls Gemini and returns structured suggestions.

    Args:
        resume_text: Extracted resume text
        job_description: Job description text
        match_result: Output from calculate_match()

    Returns:
        Dictionary with AI suggestions, or error information
        """
    max_retries = 2
    last_error = None

    for _ in range(max_retries):
        try:
            model = get_gemini_client()

            prompt = build_prompt(resume_text, job_description, match_result)

            response = model.chat.completions.create( #actual API call to Gemini
                model="llama3.2:3b",
                messages=[{"role": "user", "content": prompt}]
            )

            raw_text = response.choices[0].message.content.strip()

            if raw_text.startswith("```"):
                raw_text = raw_text.split("\n", 1)[1]   # remove first line
                raw_text = raw_text.rsplit("```", 1)[0]  # remove closing fence
                raw_text = raw_text.strip()

            suggestions = json.loads(raw_text)

            return {
                "success": True,
                "suggestions": suggestions,
                "error": None
            }

        except ValueError as e:
            return {
                "success": False,
                "suggestions": None,
                "error": f"Configuration error: {str(e)}"
            }

        except json.JSONDecodeError as e:
            last_error = f"AI returned invalid JSON: {str(e)}"
            continue  # retry

        except Exception as e:
            last_error = f"AI service error: {str(e)}"
            continue  # retry

    return {
        "success": False,
        "suggestions": None,
        "error": last_error
    }