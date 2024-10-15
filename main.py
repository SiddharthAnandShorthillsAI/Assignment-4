from file_loader import PDFLoader, DOCXLoader, PPTLoader
from data_extractor import DataExtractor
from storage import Storage, StorageSQL

def process_file(loader_class, db_path, base_output_folder):
    """
    Process a file with the specified loader, extracting data and saving it to both a database and the local filesystem.

    Args:
        loader_class: An instance of a file loader (PDFLoader, DOCXLoader, or PPTLoader) initialized with the file path.
        db_path: Path to the SQLite database for storing extracted data.
        base_output_folder: Directory path where extracted data will be saved on the filesystem.
    """
    extractor = DataExtractor(loader_class)
    
    sql_storage = StorageSQL(extractor, db_path)
    
    sql_storage.save_text()          
    sql_storage.save_links()         
    sql_storage.save_images()        
    sql_storage.save_tables()        
    sql_storage.save_metadata()      
    sql_storage.close()              

    fs_storage = Storage(extractor, base_output_folder)
    
    fs_storage.save_text()          # Store extracted text locally
    fs_storage.save_links()         # Store hyperlinks in a local file
    fs_storage.save_images()        # Store images in the output directory
    fs_storage.save_tables()        # Store table data locally
    fs_storage.save_metadata()      # Save metadata information locally


def main():
    """
    Main function that defines file paths and initiates the extraction process for each file type.
    """
    # Define paths to input files and output directories
    pdf_file = '/home/shtlp_0041/Desktop/extractionofdata/input/Document 2.pdf'
    docx_file = '/home/shtlp_0041/Desktop/extractionofdata/input/Document 2.docx'
    ppt_file = '/home/shtlp_0041/Desktop/extractionofdata/input/Document 2.pptx'
    base_output_folder = 'extracted_output'  # Folder where extracted data will be saved
    db_path = 'extracted_data.db'       # SQLite database file for saving extracted data

    # Process each file type using the appropriate loader (PDF, DOCX, PPT)
    process_file(PDFLoader(pdf_file), db_path, base_output_folder)
    process_file(DOCXLoader(docx_file), db_path, base_output_folder)
    process_file(PPTLoader(ppt_file), db_path, base_output_folder)

# If the script is executed directly, call the main function to begin processing
if __name__ == "__main__":
    main()
