import unittest
import os
from storage.file_storage import FileStorage
from extractor.data_extractor import DataExtractor
from loaders.pdf_loader import PDFLoader

class TestFileStorage(unittest.TestCase):

    def setUp(self):
        self.loader = PDFLoader('test.pdf')
        self.extractor = DataExtractor(self.loader)
        self.file_storage = FileStorage(self.extractor)

    def test_store_text(self):
        self.file_storage.store()
        self.assertTrue(os.path.exists('extracted_text.txt'))

    def test_store_csv(self):
        self.file_storage.store()
        self.assertTrue(os.path.exists('extracted_tables.csv'))

    def test_store_images(self):
        self.file_storage.store()
        # Check for images saved in your specific way
        # This is just a placeholder; you need to replace with your actual image saving logic
        images = self.extractor.extract_images()
        self.assertGreater(len(images), 0)

if __name__ == '__main__':
    unittest.main()