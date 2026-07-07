import pdfplumber
import os
import re
from app.extractors.base import BaseExtractor


class PDFExtractor(BaseExtractor):
    """Extracts text from PDF files using pdfplumber."""

    def extract(self, file_path: str) -> dict:
        if not os.path.exists(file_path):
            return {
                "success": False,
                "text": "",
                "page_count": 0,
                "error": f"File not found: {file_path}"
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
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        cleaned = self._clean_text(page_text)
                        if cleaned:
                            extracted_pages.append(cleaned)

                full_text = "\n\n".join(extracted_pages)

                if not full_text.strip():
                    return {
                        "success": False,
                        "text": "",
                        "page_count": page_count,
                        "error": (
                            "No text could be extracted. "
                            "This PDF may be scanned or image-based."
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

    def _clean_text(self, raw_text: str) -> str:
        """Cleans raw extracted text."""
        if not raw_text:
            return ""
        lines = raw_text.split("\n")
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            line = re.sub(r'\s+', ' ', line)
            if line:
                cleaned_lines.append(line)
        return "\n".join(cleaned_lines)

    def extract_hyperlinks(self, file_path: str) -> dict:
        """Extracts hyperlinks from PDF annotation layer."""
        result = {"linkedin": None, "github": None, "other_links": []}

        if not os.path.exists(file_path):
            return result

        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    for link in page.hyperlinks:
                        uri = link.get("uri", "")
                        if not uri:
                            continue
                        uri_lower = uri.lower()
                        if "linkedin.com" in uri_lower and result["linkedin"] is None:
                            result["linkedin"] = uri
                        elif "github.com" in uri_lower and result["github"] is None:
                            result["github"] = uri
                        else:
                            if uri not in result["other_links"]:
                                result["other_links"].append(uri)
        except Exception:
            pass

        return result