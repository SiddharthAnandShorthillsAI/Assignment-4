# Concrete PPTLoader Class
import os
from pptx import Presentation
from loaders.file_loader import FileLoader
class PPTLoader(FileLoader):
    """Implementation of FileLoader specifically for PPTX files."""
    
    def __init__(self, file_path: str):
        """
        Initialize the PPTLoader with the path of a PPTX file.

        Args:
            file_path (str): The full path to the PPTX file.
        """
        self.file_path = file_path
        self.content = None


    def load_file(self):
        """
        Load the PPTX file and retrieve its content.

        Returns:
            Presentation: The Presentation object representing the loaded PPTX file.

        Raises:
            ValueError: If the file is not a valid PPTX file.
        """
        if self.validate_file():
            self.content = Presentation(self.file_path)  # Load the content of the PPTX file
            return self.content
        raise ValueError("Invalid PPT file")
