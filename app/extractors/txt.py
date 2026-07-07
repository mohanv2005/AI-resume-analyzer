import os
from app.extractors.base import BaseExtractor


class TXTExtractor(BaseExtractor):
    """
    Extracts text from plain .txt files.
    Simplest extractor — just reads the file content directly.
    """

    def extract(self, file_path: str) -> dict:
        if not os.path.exists(file_path):
            return {
                "success": False,
                "text": "",
                "page_count": 0,
                "error": f"File not found: {file_path}"
            }

        try:
            # Try UTF-8 first (most common encoding)
            # Fall back to latin-1 which handles most Western text
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
            except UnicodeDecodeError:
                with open(file_path, "r", encoding="latin-1") as f:
                    text = f.read()

            if not text.strip():
                return {
                    "success": False,
                    "text": "",
                    "page_count": 1,
                    "error": "Text file is empty."
                }

            return {
                "success": True,
                "text": text.strip(),
                "page_count": 1,
                "error": None
            }

        except Exception as e:
            return {
                "success": False,
                "text": "",
                "page_count": 0,
                "error": f"Failed to read text file: {str(e)}"
            }