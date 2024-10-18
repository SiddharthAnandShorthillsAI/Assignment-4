import os
from pdfminer.high_level import extract_text
import pdfplumber
from pdf2image import convert_from_path
import pytesseract #wrapper for Google's Tesseract-OCR engine, used for optical character recognition
#(OCR) to extract text from images.
from loaders.file_loader import FileLoader
class PDFLoader(FileLoader):
    """Implementation of FileLoader for PDF files."""
    
    def __init__(self, file_path: str):
        """
        Initialize the PDFLoader with the path of a PDF file.

        Args:
            file_path (str): The full path to the PDF file.
        """
        self.file_path = file_path

    def validate_file(self) -> bool:
        """Check if the provided path points to a valid PDF file."""
        return self.file_path.endswith('.pdf') and os.path.isfile(self.file_path)

    def load_file(self):
        """
        Load the PDF file and extract its text content.

        Returns:
            str: The text extracted from the PDF file.

        Raises:
            ValueError: If the file is invalid or text extraction encounters an error.
        """
        if not self.validate_file():
            raise ValueError("Invalid PDF file")

        # Attempt text extraction using pdfminer
        try:
            text = extract_text(self.file_path)
            if text.strip():
                return text
            else:   #switches to ocr to extract text 
                print("No text found in PDF using pdfminer; switching to OCR.")
        except Exception as e: #if OCR fails then raise exception
            print(f"Error during text extraction with pdfminer: {e}; switching to OCR.")

        # Use OCR as a fallback if pdfminer extraction fails
        try:
            return self.extract_text_with_ocr()
        except Exception as e:
            print(f"Error during OCR extraction: {e}")
            raise ValueError("Failed to extract text from PDF.")

    def extract_text_with_ocr(self):
        """Convert the PDF pages to images and apply OCR to extract text.

        Returns:
            str: The text obtained from the PDF images via OCR.
        """
        images = convert_from_path(self.file_path)  # Convert each page of the PDF to an image
        text = ""
        for image in images:
            try:
                ocr_text = pytesseract.image_to_string(image)  # Perform OCR to extract text
                text += ocr_text
            except Exception as e:
                print(f"Error during OCR on one of the pages: {e}")
        return text

    def extract_links(self):
        """Retrieve hyperlinks embedded in the PDF file.

        Returns:
            list: A list containing all hyperlinks found in the PDF.
        """
        links = []
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                if page.annots:  # Check for annotations on the page
                    for annotation in page.annots:
                        if annotation.get("uri"):
                            links.append(annotation["uri"])  # Add hyperlink to the list
        return links

    def extract_images(self):
        """Extract images embedded within the PDF file.

        Returns:
            list: A collection of image metadata from the PDF.
        """
        images = []
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                if page.images:
                    images.extend(page.images)  # Collect image metadata
        return images

    def extract_tables(self):
        """Extract tabular data present in the PDF.

        Returns:
            list: A list of tables obtained from the PDF.
        """
        tables = []
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                tables.extend(page.extract_tables())  # Gather all tables from each page
        return tables
    
    def extract_metadata(self):
        """Extract metadata information from the PDF file.

        Returns:
            dict: A dictionary containing key metadata fields of the PDF.
        """
        metadata = {}
        with pdfplumber.open(self.file_path) as pdf:
            metadata = pdf.metadata  # Fetch metadata using pdfplumber
        return metadata
    