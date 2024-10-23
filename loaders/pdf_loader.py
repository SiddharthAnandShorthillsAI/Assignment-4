from pdfminer.high_level import extract_text
from pdf2image import convert_from_path
from loaders.file_loader import FileLoader
class PDFLoader(FileLoader):
    """Implementation of FileLoader for PDF files."""
    
    def __init__(self, file_path: str):
        """
        Initialize the PDFLoader with the path of a PDF file.

        Args:
            file_path (str): The full path to the PDF file.
        """
        self.file_path = file_path

    def load_file(self):
        """
        Load the PDF file and extract its text content.

        Returns:
            str: The text extracted from the PDF file.

        Raises:
            ValueError: If the file is invalid or text extraction encounters an error.
        """
        if not self.validate_file():
            raise ValueError("Invalid PDF file")
        
        return self.file_path
