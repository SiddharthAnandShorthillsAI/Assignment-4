from abc import ABC, abstractmethod
import os
# Abstract Class for File Loading
class FileLoader(ABC):
    """Abstract class defining the interface for loading various file types.""" 
    def validate_file(self) -> bool:
        """Verify if the file is valid."""
        return os.path.isfile(self.file_path)
        pass
    @abstractmethod
    def load_file(self):
        """Load the file and retrieve its content."""
        pass
