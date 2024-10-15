
import unittest
from unittest.mock import MagicMock
import os
import shutil
import sqlite3
from data_extractor import DataExtractor
from file_loader import PDFLoader, DOCXLoader, PPTLoader
from storage import Storage, StorageSQL
from unittest import mock

class TestStorage(unittest.TestCase):

    def setUp(self):         
        self.base_path = 'test_output_data'
        self.db_path = 'test_extracted_data.db'

        # Create mock file loaders
        self.pdf_loader = PDFLoader('sample.pdf')
        self.docx_loader = DOCXLoader('sample.docx')
        self.ppt_loader = PPTLoader('sample.pptx')
        
        self.pdf_extractor = DataExtractor(self.pdf_loader)
        self.docx_extractor = DataExtractor(self.docx_loader)
        self.ppt_extractor = DataExtractor(self.ppt_loader)
        
        self.storage_pdf = Storage(self.pdf_extractor, self.base_path)
        self.storage_sql_pdf = StorageSQL(self.pdf_extractor, self.db_path)

        self.storage_docx = Storage(self.docx_extractor, self.base_path)
        self.storage_sql_docx = StorageSQL(self.docx_extractor, self.db_path)

        self.storage_ppt = Storage(self.ppt_extractor, self.base_path)
        self.storage_sql_ppt = StorageSQL(self.ppt_extractor, self.db_path)

    def tearDown(self):
        if os.path.exists(self.base_path):
            shutil.rmtree(self.base_path)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)




class TestFileProcessing(unittest.TestCase):

    def setUp(self):
        """Setup common variables for testing"""
        self.db_path = 'test_extracted_data.db'  # SQLite DB for test
        self.base_output_folder = 'test_output_data'  # Filesystem storage for test output
        if not os.path.exists(self.base_output_folder):
            os.mkdir(self.base_output_folder)
    
    def tearDown(self):
        """Clean up after each test"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        if os.path.exists(self.base_output_folder):
            for file in os.listdir(self.base_output_folder):
                os.remove(os.path.join(self.base_output_folder, file))
            os.rmdir(self.base_output_folder)

    def test_TC_011_valid_file_path_pdf(self):
        """Test valid PDF file path for loading"""
        pdf_file = 'sample.pdf'
        loader = PDFLoader(pdf_file)
        self.assertIsInstance(loader, PDFLoader, "PDF file should load with a valid path.")

    def test_TC_010_valid_file_path_pdf(self):
        """Test valid PDF file path for loading"""
        pdf_file = 'Document 2.docx'
        loader = DOCXLoader(pdf_file)
        self.assertIsInstance(loader, DOCXLoader, "PDF file should load with a valid path.")

    def test_TC_018_valid_file_path_pdf(self):
        """Test valid PDF file path for loading"""
        pdf_file = 'Document 2.pptx'
        loader = PPTLoader(pdf_file)
        self.assertIsInstance(loader, PPTLoader, "PDF file should load with a valid path.")

    def test_TC_028_invalid_file_path(self):
        """Test invalid file path handling for PDF."""
        invalid_file = 'invalid_file.pdf'  # File that does not exist or is corrupted
        with self.assertRaises(ValueError, msg="Invalid PDF file should raise ValueError"):
            loader = PDFLoader(invalid_file)
            loader.load_file()  # This should raise the ValueError based on your error output

    def test_TC_029_invalid_file_path(self):
        """Test invalid file path handling for PDF."""
        invalid_file = 'invalid_file.docx'  # File that does not exist or is corrupted
        with self.assertRaises(ValueError, msg="Invalid PDF file should raise ValueError"):
            loader = DOCXLoader(invalid_file)
            loader.load_file()  # This should raise the ValueError based on your error output

    def test_TC_02_invalid_file_path(self):
        """Test invalid file path handling for PDF."""
        invalid_file = 'invalid_file.pptx'  # File that does not exist or is corrupted
        with self.assertRaises(ValueError, msg="Invalid PDF file should raise ValueError"):
            loader = PPTLoader(invalid_file)
            loader.load_file()  # This should raise the ValueError based on your error output


    def test_TC_038_empty_file_handling_pdf(self):
        """Test empty PDF file handling"""
        empty_file = '/home/shtlp_0041/Desktop/extractionofdata/input/Emptyfile.docx'
        loader = DOCXLoader(empty_file)
        extractor = DataExtractor(loader)
        extracted_text = extractor.extract_text()
        self.assertEqual(extracted_text, "", "No content should be extracted from an empty file.")

    def test_TC_03_empty_file_handling_pdf(self):
        """Test empty PDF file handling"""
        empty_file = '/home/shtlp_0041/Desktop/extractionofdata/input/Emptyfile.pdf'
        loader = PDFLoader(empty_file)
        extractor = DataExtractor(loader)
        extracted_text = extractor.extract_text()
        self.assertEqual(extracted_text, "", "No content should be extracted from an empty file.")

    def test_TC_041_unsupported_file_type(self):
        """Test unsupported file type handling"""
        unsupported_file = 'abc.txt'
        with self.assertRaises(ValueError):
            loader = PDFLoader(unsupported_file)  # Assuming unsupported types raise ValueError
            loader.load_file()

    def test_TC_047_unsupported_file_type(self):
        """Test unsupported file type handling"""
        unsupported_file = 'abc.txt'
        with self.assertRaises(ValueError):
            loader = PPTLoader(unsupported_file)  # Assuming unsupported types raise ValueError
            loader.load_file()

    def test_TC_04_unsupported_file_type(self):
        """Test unsupported file type handling"""
        unsupported_file = 'abc.txt'
        with self.assertRaises(ValueError):
            loader = DOCXLoader(unsupported_file)  # Assuming unsupported types raise ValueError
            loader.load_file()

    def test_TC_05_text_extraction_from_pdf(self):
        """Test text extraction from PDF"""
        pdf_file = '/home/shtlp_0041/Desktop/extractionofdata/Document 2.pdf'
        loader = PDFLoader(pdf_file)
        extractor = DataExtractor(loader)
        extracted_text = extractor.extract_text()
        self.assertTrue(len(extracted_text) > 0, "Text should be extracted from the PDF file.")

    def test_TC_06_text_extraction_from_docx(self):
        """Test text extraction from DOCX"""
        docx_file = '/home/shtlp_0041/Desktop/extractionofdata/Document 2.docx'
        loader = DOCXLoader(docx_file)
        extractor = DataExtractor(loader)
        extracted_text = extractor.extract_text()
        self.assertTrue(len(extracted_text) > 0, "Text should be extracted from the DOCX file.")

    def test_TC_07_text_extraction_from_ppt(self):
        """Test text extraction from PPT"""
        ppt_file = 'Document 2.pptx'
        loader = PPTLoader(ppt_file)
        extractor = DataExtractor(loader)
        extracted_text = extractor.extract_text()
        self.assertTrue(len(extracted_text) > 0, "Text should be extracted from the PPT file.")

    def test_TC_088_text_extraction_special_characters(self):
        """Test extraction of text with special characters"""
        docx_file = '/home/shtlp_0041/Desktop/extractionofdata/input/special.pdf'
        loader = PDFLoader(docx_file)
        extractor = DataExtractor(loader)
        extracted_text = extractor.extract_text()
        self.assertIn("&", extracted_text, "Special characters should be extracted correctly.")

    def test_TC_08_text_extraction_special_characters(self):
        """Test extraction of text with special characters"""
        docx_file = '/home/shtlp_0041/Desktop/extractionofdata/input/special.docx'
        loader = DOCXLoader(docx_file)
        extractor = DataExtractor(loader)
        extracted_text = extractor.extract_text()
        self.assertIn("$", extracted_text, "Special characters should be extracted correctly.")

   

    def test_TC_09_text_extraction_from_multipage_pdf(self):
        """Test extraction of text from multi-page PDF"""
        pdf_file = '/home/shtlp_0041/Desktop/extractionofdata/Document 2.pdf'
        loader = PDFLoader(pdf_file)
        extractor = DataExtractor(loader)
        extracted_text = extractor.extract_text()
        self.assertTrue(len(extracted_text.split()) > 100, "Text from multiple pages should be extracted.")

    '''def test_TC_099_text_extraction_from_multipage_pdf(self):
        """Test extraction of text from multi-page PDF"""
        pdf_file = 'Document 2 1.pptx'
        loader = PPTLoader(pdf_file)
        extractor = DataExtractor(loader)
        extracted_text = extractor.extract_text()
        self.assertTrue(len(extracted_text.split()) > 100, "Text from multiple pages should be extracted.")'''

    def test_TC_10_link_extraction_from_pdf(self):
        """Test link extraction from PDF"""
        pdf_file = '/home/shtlp_0041/Desktop/extractionofdata/Document 2.pdf'
        loader = PDFLoader(pdf_file)
        extractor = DataExtractor(loader)
        extracted_links = extractor.extract_links()
        self.assertGreater(len(extracted_links), 0, "Links should be extracted from the PDF file.")

    def test_TC_11_link_extraction_from_docx(self):
        """Test link extraction from DOCX"""
        docx_file = 'Document 2.docx'
        loader = DOCXLoader(docx_file)
        extractor = DataExtractor(loader)
        extracted_links = extractor.extract_links()
        self.assertGreater(len(extracted_links), 0, "Links should be extracted from the DOCX file.")

    def test_TC_12_link_extraction_from_ppt(self):
        """Test link extraction from PPT"""
        ppt_file = 'Document 2.pptx'
        loader = PPTLoader(ppt_file)
        extractor = DataExtractor(loader)
        extracted_links = extractor.extract_links()
        self.assertGreater(len(extracted_links), 0, "Links should be extracted from the PPT file.")

    def test_TC_18_image_extraction_from_pdf(self):
        """Test image extraction from PDF"""
        pdf_file = '/home/shtlp_0041/Desktop/extractionofdata/Document 2.pdf'
        loader = PDFLoader(pdf_file)
        extractor = DataExtractor(loader)
        extracted_images = extractor.extract_images()
        self.assertGreater(len(extracted_images), 0, "Images should be extracted from the PDF file.")

    def test_TC_18_image_extraction_from_ppt(self):
        """Test image extraction from PDF"""
        pdf_file = '/home/shtlp_0041/Desktop/extractionofdata/Document 2.pptx'
        loader = PPTLoader(pdf_file)
        extractor = DataExtractor(loader)
        extracted_images = extractor.extract_images()
        self.assertGreater(len(extracted_images), 0, "Images should be extracted from the PDF file.")

    def test_TC_18_image_extraction_from_docs(self):
        """Test image extraction from PDF"""
        pdf_file = '/home/shtlp_0041/Desktop/extractionofdata/Document 2.docx'
        loader = DOCXLoader(pdf_file)
        extractor = DataExtractor(loader)
        extracted_images = extractor.extract_images()
        self.assertGreater(len(extracted_images), 0, "Images should be extracted from the PDF file.")

    def test_TC_13_table_extraction_from_pdf(self):
        """Test table extraction from PDF."""
        valid_pdf_with_tables = '/home/shtlp_0041/Desktop/extractionofdata/Document 2.pdf'  # Sample PDF containing tables
        loader = PDFLoader(valid_pdf_with_tables)
        extractor = DataExtractor(loader)
        tables = extractor.extract_tables()
        self.assertIsNotNone(tables, msg="Tables should be extracted from the PDF")
        self.assertGreater(len(tables), 0, msg="There should be at least one table extracted from the PDF")

    def test_TC_14_table_extraction_from_docx(self):
        """Test table extraction from DOCX."""
        valid_docx_with_tables = '/home/shtlp_0041/Desktop/extractionofdata/Document 2.docx'  # Sample DOCX with tables
        loader = DOCXLoader(valid_docx_with_tables)
        extractor = DataExtractor(loader)
        tables = extractor.extract_tables()
        self.assertIsNotNone(tables, msg="Tables should be extracted from the DOCX")
        self.assertGreater(len(tables), 0, msg="At least one table should be extracted from the DOCX")

    def test_TC_14_table_extraction_from_ppt(self):
        """Test table extraction from DOCX."""
        valid_docx_with_tables = '/home/shtlp_0041/Desktop/extractionofdata/Document 2.pptx'  # Sample DOCX with tables
        loader = PPTLoader(valid_docx_with_tables)
        extractor = DataExtractor(loader)
        tables = extractor.extract_tables()
        self.assertIsNotNone(tables, msg="Tables should be extracted from the DOCX")
        self.assertGreater(len(tables), 0, msg="At least one table should be extracted from the DOCX")

    def test_TC_20_mixed_content_extraction(self):
        """Test extraction of mixed content (text and images) from a file."""
        valid_docx_with_mixed_content = '/home/shtlp_0041/Desktop/extractionofdata/Document 2.docx'  # DOCX with both text and images
        loader = DOCXLoader(valid_docx_with_mixed_content)
        extractor = DataExtractor(loader)
        
        text = extractor.extract_text()
        images = extractor.extract_images()
        
        self.assertIsNotNone(text, msg="Text should be extracted from the DOCX")
        self.assertIsNotNone(images, msg="Images should be extracted from the DOCX")
        self.assertGreater(len(images), 0, msg="There should be at least one image extracted")

    def test_TC_229_save_text_to_local_storage(self):
        """Test saving extracted text data to local storage."""
        valid_pdf_with_text = '/home/shtlp_0041/Desktop/extractionofdata/Document 2.pdf'  # PDF containing text
        loader = PDFLoader(valid_pdf_with_text)
        extractor = DataExtractor(loader)
        storage = Storage(extractor, 'output_folder')  # Define output folder path
        
        storage.save_text()  # Save extracted text to local storage
        self.assertTrue(os.path.exists('output_folder/text/pdf_text.txt'), msg="Text data should be saved to local storage")

    def test_TC_22_sa9ve_text_to_local_storage(self):
        """Test saving extracted text data to local storage."""
        valid_pdf_with_text = '/home/shtlp_0041/Desktop/extractionofdata/Document 2.pptx'  # PDF containing text
        loader = PPTLoader(valid_pdf_with_text)
        extractor = DataExtractor(loader)
        storage = Storage(extractor, 'output_folder')  # Define output folder path
        
        storage.save_text()  # Save extracted text to local storage
        self.assertTrue(os.path.exists('output_folder/text/ppt_text.txt'), msg="Text data should be saved to local storage")

    def test_TC_22_save_text_to_local_storage(self):
        """Test saving extracted text data to local storage."""
        valid_pdf_with_text = '/home/shtlp_0041/Desktop/extractionofdata/Document 2.docx'  # PDF containing text
        loader = DOCXLoader(valid_pdf_with_text)
        extractor = DataExtractor(loader)
        storage = Storage(extractor, 'output_folder')  
        
        storage.save_text()  
        self.assertTrue(os.path.exists('output_folder/text/docx_text.txt'), msg="Text data should be saved to local storage")

    def test_TC_23_save_images_to_local_storage(self):
        """Test saving extracted images to local storage."""
        valid_pdf_with_images = '/home/shtlp_0041/Desktop/extractionofdata/Document 2.pdf'
        loader = PDFLoader(valid_pdf_with_images)
        extractor = DataExtractor(loader)
        storage = Storage(extractor, 'output_folder')
        
        storage.save_images()  # Save extracted images to the filesystem
        self.assertTrue(os.path.exists('output_folder/images'), msg="Images should be saved in the local storage")
        self.assertGreater(len(os.listdir('output_folder/images')), 0, msg="There should be images saved in the folder")

    def test_TC_24_save_links_to_local_storage(self):
        """Test saving extracted hyperlinks to local storage."""
        valid_pdf_with_links = '/home/shtlp_0041/Desktop/extractionofdata/Document 2.pdf'  
        loader = PDFLoader(valid_pdf_with_links)
        extractor = DataExtractor(loader)
        storage = Storage(extractor, 'output_folder')
        
        storage.save_links() 
        self.assertFalse(os.path.exists('output_folder/pdf_links.txt'), msg="Links should be saved to local storage")



if __name__ == '__main__':
    unittest.main()
