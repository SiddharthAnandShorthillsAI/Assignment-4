from abc import ABC, abstractmethod

class FileLoader(ABC):
    def __init__(self, file_path):
        self.file_path = file_path
        self.validate()

    @abstractmethod
    def validate(self):
        """Validate the file type."""
        pass

    @abstractmethod
    def load_file(self):
        """Load the file for processing."""
        pass