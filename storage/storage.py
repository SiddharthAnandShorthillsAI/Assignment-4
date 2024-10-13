from abc import ABC, abstractmethod

class Storage(ABC):
    def __init__(self, extractor):
        self.extractor = extractor

    @abstractmethod
    def store(self):
        """Store the extracted data."""
        pass