from abc import ABC, abstractmethod
import os
from pdfminer.high_level import extract_text
import pdfplumber
from docx import Document
from pptx import Presentation
from pdf2image import convert_from_path
import pytesseract
# Abstract Class for File Loading
class FileLoader(ABC):
    """Abstract class defining the interface for loading various file types.""" 
    @abstractmethod
    def validate_file(self) -> bool:
        """Verify if the file is valid."""
        pass
    @abstractmethod
    def load_file(self):
        """Load the file and retrieve its content."""
        pass
