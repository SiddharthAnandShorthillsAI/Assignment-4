import unittest
import os
from loaders.pdf_loader import PDFLoader
from loaders.docs_loader import DOCXLoader
from loaders.ppt_loader import PPTLoader

from extractor.data_extractor import DataExtractor

class TestDataExtractor(unittest.TestCase):

    def setUp(self):
        # Check if test files exist
        self.pdf_path = 'test.pdf'
        self.docx_path = 'test.docx'
        self.ppt_path = 'test.pptx'

        if not (os.path.exists(self.pdf_path) and os.path.exists(self.docx_path) and os.path.exists(self.ppt_path)):
            self.skipTest("Test files are missing. Ensure test.pdf, test.docx, and test.pptx are in the correct location.")

        self.pdf_loader = PDFLoader(self.pdf_path)
        self.docx_loader = DOCXLoader(self.docx_path)
        self.ppt_loader = PPTLoader(self.ppt_path)

        self.pdf_extractor = DataExtractor(self.pdf_loader)
        self.docx_extractor = DataExtractor(self.docx_loader)
        self.ppt_extractor = DataExtractor(self.ppt_loader)

    def test_extract_text_pdf(self):
        text = self.pdf_extractor.extract_text()
        self.assertIsInstance(text, str)
        self.assertTrue(len(text) > 0, "Extracted text should not be empty")

    def test_extract_text_docx(self):
        text = self.docx_extractor.extract_text()
        self.assertIsInstance(text, str)
        self.assertTrue(len(text) > 0, "Extracted text should not be empty")

    def test_extract_text_ppt(self):
        text = self.ppt_extractor.extract_text()
        self.assertIsInstance(text, str)
        self.assertTrue(len(text) > 0, "Extracted text should not be empty")

    def test_extract_links_pdf(self):
        links = self.pdf_extractor.extract_links()
        self.assertIsInstance(links, list)

    def test_extract_links_docx(self):
        links = self.docx_extractor.extract_links()
        self.assertIsInstance(links, list)

    def test_extract_links_ppt(self):
        links = self.ppt_extractor.extract_links()
        self.assertIsInstance(links, list)

    def test_extract_images_pdf(self):
        images = self.pdf_extractor.extract_images()
        self.assertIsInstance(images, list)

    def test_extract_images_docx(self):
        images = self.docx_extractor.extract_images()
        self.assertIsInstance(images, list)

    def test_extract_images_ppt(self):
        images = self.ppt_extractor.extract_images()
        self.assertIsInstance(images, list)

    def test_extract_tables_pdf(self):
        tables = self.pdf_extractor.extract_tables()
        self.assertIsInstance(tables, list)

    def test_extract_tables_docx(self):
        tables = self.docx_extractor.extract_tables()
        self.assertIsInstance(tables, list)

    def test_extract_tables_ppt(self):
        tables = self.ppt_extractor.extract_tables()
        self.assertIsInstance(tables, list)

if __name__ == '__main__':
    unittest.main()