
import pdfplumber          # For PDF text extraction
import os                  # For file path operations
import re                  # For regex-based cleaning
from typing import Optional  # For type hints where a value might be None


def extract_text_from_pdf(file_path: str) -> dict:
    """
    Extracts and cleans text from a PDF file.

    Args:
        file_path: Absolute or relative path to the PDF file

    Returns:
        A dictionary containing:
            - success (bool): whether extraction worked
            - text (str): the extracted and cleaned text
            - page_count (int): number of pages in the PDF
            - error (str | None): error message if extraction failed
    """

    if not os.path.exists(file_path):
        return {
            "success": False,
            "text": "",
            "page_count": 0,
            "error": f"File not found: {file_path}"
        }

    if not file_path.lower().endswith(".pdf"):
        return {
            "success": False,
            "text": "",
            "page_count": 0,
            "error": "File is not a PDF"
        }

    try:
        with pdfplumber.open(file_path) as pdf:

            page_count = len(pdf.pages)

            if page_count == 0:
                return {
                    "success": False,
                    "text": "",
                    "page_count": 0,
                    "error": "PDF has no pages"
                }

            extracted_pages = [] 

            for page_number, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text()

                if page_text:
                    cleaned = clean_text(page_text)
                    if cleaned:
                        extracted_pages.append(cleaned)

            # Combine all pages 
            full_text = "\n\n".join(extracted_pages)

            # Guard: PDF opened fine but no text could be extracted
            # This happens with scanned PDFs (image-only, no text layer)
            if not full_text.strip():
                return {
                    "success": False,
                    "text": "",
                    "page_count": page_count,
                    "error": (
                        "No text could be extracted. "
                        "This PDF may be scanned or image-based. "
                        "Please upload a text-based PDF."
                    )
                }

            return {
                "success": True,
                "text": full_text,
                "page_count": page_count,
                "error": None
            }

    except Exception as e:
        return {
            "success": False,
            "text": "",
            "page_count": 0,
            "error": f"Failed to extract text from PDF: {str(e)}"
        }


def clean_text(raw_text: str) -> str:
    """
    Cleans raw extracted PDF text by removing noise and normalizing whitespace.

    Args:
        raw_text: The messy raw string from pdfplumber

    Returns:
        A cleaned, normalized string
    """

    if not raw_text:
        return ""

    lines = raw_text.split("\n")

    cleaned_lines = []
    for line in lines:
        line = line.strip()

        line = re.sub(r'\s+', ' ', line)

        if line:
            cleaned_lines.append(line)

    cleaned = "\n".join(cleaned_lines)

    return cleaned


def get_text_stats(text: str) -> dict:
    """
    Returns basic statistics about the extracted text.
    Useful for debugging and understanding resume content.

    Args:
        text: Cleaned text string

    Returns:
        Dictionary with word_count, line_count, char_count
    """
    if not text:
        return {"word_count": 0, "line_count": 0, "char_count": 0}

    lines = text.split("\n")
    words = text.split()     

    return {
        "word_count": len(words),
        "line_count": len(lines),
        "char_count": len(text)
    }

def extract_email(text: str) -> Optional[str]:
    """
    Extracts the first email address found in the text using regex.

    Args:
        text: The cleaned text string
    """
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(pattern, text)

    if match:
        return match.group().lower()
    return None

def extract_phone_number(text: str) -> Optional[str]:
    """
    Extracts the first phone number found in the text using regex.
    Supports various formats, including international.

    Args:
        text: The cleaned text string
    """
    pattern = r"(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}"
    match = re.search(pattern, text)

    if match:
        raw = match.group().strip()
        return raw
    return None

def extract_github_link(text: str) -> Optional[str]:
    """
    Extracts the first GitHub link found in the text using regex.

    Args:
        text: The cleaned text string
    """
    pattern = r"(https?://)?(www\.)?github\.com/[\w\-]+"
    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group()
    return None

def extract_linkedin_link(text: str) -> Optional[str]:
    """
    Extracts the first LinkedIn link found in the text using regex.

    Args:
        text: The cleaned text string
    """
    pattern = r"(https?://)?(www\.)?linkedin\.com/in/[\w\-]+"
    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return match.group()
    return None

