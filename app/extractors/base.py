class BaseExtractor:
    """
    Abstract base class for all file extractors.
    Every extractor must implement the extract() method.
    This ensures all extractors have the same interface,
    so the rest of the app doesn't care what file type it's dealing with.
    """

    def extract(self, file_path: str) -> dict:
        """
        Extract text from a file.

        Args:
            file_path: Path to the file on disk

        Returns:
            Dictionary with:
                - success (bool)
                - text (str)
                - page_count (int)
                - error (str | None)
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement extract()"
        )