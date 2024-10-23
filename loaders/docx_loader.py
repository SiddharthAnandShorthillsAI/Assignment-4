# Concrete DOCXLoader Class
from docx import Document
from loaders.file_loader import FileLoader
class DOCXLoader(FileLoader):
    """Implementation of FileLoader specifically for DOCX files."""
    
    def __init__(self, file_path: str):
        """
        Initialize the DOCXLoader with the path of a DOCX file.

        Args:
            file_path (str): The full path to the DOCX file.
        """
        self.file_path = file_path
        self.content = None


    def load_file(self):
        """
        Load the DOCX file and retrieve its content.

        Returns:
            Document: The Document object representing the loaded DOCX file.

        Raises:
            ValueError: If the file is not a valid DOCX file.
        """
        if self.validate_file():
            self.content = Document(self.file_path)  # Load the content of the DOCX file
            return self.content
        raise ValueError("Invalid DOCX file")
    
