import pptx  # python-pptx for PPTX files
from .file_loader import FileLoader

class PPTLoader(FileLoader):
    def validate(self):
        if not self.file_path.endswith('.pptx'):
            raise ValueError("Invalid file type: Expected a PPTX file.")

    def load_file(self):
        return pptx.Presentation(self.file_path)  # Load PPTX document