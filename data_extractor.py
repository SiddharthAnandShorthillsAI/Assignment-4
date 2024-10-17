from loaders.pdf_loader import PDFLoader
from loaders.docx_loader import DOCXLoader
from loaders.ppt_loader import  PPTLoader
from docx.opc.constants import RELATIONSHIP_TYPE as RT

class DataExtractor:
#    class for extracting images , text , links ,tables 
    def __init__(self, file_loader):
        """
Initialize the DataExtractor with the specified file loader.
 Arguments:   file_loader: An instance of a loader class (e.g., PDFLoader, DOCXLoader, or PPTLoader) responsible for loading and handling file content.
"""
        self.file_loader = file_loader 
        self.content = self.file_loader.load_file()
        
    def extract_links(self):       
        """
Extracts hyperlinks from the loaded file, based on the file type.

This method handles different file types by delegating the extraction process to the appropriate file loader:

- For PDFs, it calls the `extract_links` method of the PDFLoader.
- For DOCX documents, it extracts the hyperlink targets from the document relationships.
- For PPT presentations, it retrieves hyperlinks from the text frames of each slide, returning both the link text and the address.

Returns:
    list: A list of hyperlinks. For PPT files, this list contains tuples in the format (link text, link address).
"""
        if isinstance(self.file_loader, PDFLoader):      
            return self.file_loader.extract_links()  # Extract links from a PDF
        links = []
        if isinstance(self.file_loader, DOCXLoader):
            for rel in self.content.part.rels.values():
                if rel.reltype == RT.HYPERLINK:
                    links.append(rel._target)  # Add the target of the hyperlink
        elif isinstance(self.file_loader, PPTLoader):               # Extract hyperlinks from each slide in a PPT presentation
            for slide in self.content.slides:
                for shape in slide.shapes:
                    if shape.has_text_frame:
                        for paragraph in shape.text_frame.paragraphs:
                            for run in paragraph.runs:
                                if run.hyperlink and run.hyperlink.address:
                                    links.append((run.text, run.hyperlink.address))  # Add text and address as a tuple
        return links
    def extract_text(self):
        """
        Extract text content from the loaded file.

        Returns:
            str: The extracted text as a single string.
        """
        if isinstance(self.file_loader, PDFLoader): # return PDF content
            return self.content  
        elif isinstance(self.file_loader, DOCXLoader):
            # Join all paragraph texts in a DOCX document
            return '\n'.join(paragraph.text for paragraph in self.content.paragraphs)
        elif isinstance(self.file_loader, PPTLoader):
            # Join all shape texts from each slide in a PPT presentation
            return '\n'.join(
                shape.text for slide in self.content.slides for shape in slide.shapes if hasattr(shape, "text")
            )
        return ""


    def extract_images(self):
        """
        Extract the images from the loaded file.

        Returns: list: A list of image binary data.
        """
        images = []
        if isinstance(self.file_loader, PDFLoader):
            return self.file_loader.extract_images()  # Extract images from a PDF
        if isinstance(self.file_loader, DOCXLoader):
            for rel in self.content.part.rels.values():
                if "image" in rel.target_ref:
                    image_data = rel.target_part.blob
                    images.append(image_data)  
        elif isinstance(self.file_loader, PPTLoader):
            for slide in self.content.slides:
                for shape in slide.shapes:
                    if shape.shape_type == 13:  # Shape type 13 means picture
                        images.append(shape.image.blob)  
        return images

    def extract_tables(self):
        """
        Extract tables from the loaded file.

        Returns:
            list: A list of tables, where each table is represented as a list of lists (rows and columns).
        """
        if isinstance(self.file_loader, PDFLoader):
            return self.file_loader.extract_tables() 
        tables = []
        if isinstance(self.file_loader, DOCXLoader):
            for table in self.content.tables:
                table_data = [[cell.text for cell in row.cells] for row in table.rows]
                tables.append(table_data)  
        elif isinstance(self.file_loader, PPTLoader):
            for slide in self.content.slides:
                for shape in slide.shapes:
                    if shape.has_table:
                        table_data = [[cell.text for cell in row.cells] for row in shape.table.rows]
                        tables.append(table_data)  
        return tables
    def extract_metadata(self):
        """
        Extract metadata from the loaded file.

        Returns:
            dict: A dictionary containing metadata (e.g., author, title, creation date).
        """
        if isinstance(self.file_loader, PDFLoader):
            return self.file_loader.extract_metadata()  # Extract metadata from a PDF
        elif isinstance(self.file_loader, DOCXLoader):
            return self.file_loader.extract_metadata()  # Extract metadata from DOCX
        elif isinstance(self.file_loader, PPTLoader):
            return self.file_loader.extract_metadata()  # Extract metadata from PPTX
        return {}

