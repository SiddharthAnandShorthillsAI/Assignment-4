import fitz  # PyMuPDF for PDF files
from .file_loader import FileLoader

class PDFLoader(FileLoader):
    def validate(self):
        if not self.file_path.endswith('.pdf'):
            raise ValueError("Invalid file type: Expected a PDF file.")

    def load_file(self):
        return fitz.open(self.file_path)  # Load PDF document