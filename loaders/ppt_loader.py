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

    # def extract_metadata(self):
    #     """Extract metadata from the PPTX file.

    #     Returns:
    #         dict: A dictionary containing the key metadata properties of the PPTX file.
    #     """
    #     metadata = {}
    #     presentation = Presentation(self.file_path)
    #     core_properties = presentation.core_properties  # Access the core properties for metadata
    #     metadata = {
    #         'title': core_properties.title,
    #         'author': core_properties.author,
    #         'subject': core_properties.subject,
    #         'keywords': core_properties.keywords,
    #         'created': core_properties.created,
    #         'modified': core_properties.modified,
    #     }
    #     return metadata