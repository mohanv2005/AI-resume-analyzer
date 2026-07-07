import os
from app.extractors.base import BaseExtractor
from app.extractors.pdf import PDFExtractor
from app.extractors.docx import DOCXExtractor
from app.extractors.txt import TXTExtractor


SUPPORTED_CONTENT_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain"
}


def get_extractor(file_path: str) -> BaseExtractor:
    """
    Factory function — returns the right extractor based on file extension.

    Args:
        file_path: Path to the uploaded file

    Returns:
        An extractor instance that implements BaseExtractor

    Raises:
        ValueError: if file type is not supported
    """
    _, extension = os.path.splitext(file_path.lower())

    extractors = {
        ".pdf":  PDFExtractor,
        ".docx": DOCXExtractor,
        ".txt":  TXTExtractor,
    }

    if extension not in extractors:
        raise ValueError(
            f"Unsupported file type: '{extension}'. "
            f"Supported types: {', '.join(extractors.keys())}"
        )

    return extractors[extension]()


def extract_from_file(file_path: str) -> dict:
    """
    Convenience function — get extractor and extract in one call.
    This is what your endpoints will call directly.

    Args:
        file_path: Path to the uploaded file

    Returns:
        Extraction result dict with success, text, page_count, error
    """
    try:
        extractor = get_extractor(file_path)
        return extractor.extract(file_path)
    except ValueError as e:
        return {
            "success": False,
            "text": "",
            "page_count": 0,
            "error": str(e)
        }