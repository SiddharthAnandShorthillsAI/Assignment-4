from abc import ABC, abstractmethod
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
