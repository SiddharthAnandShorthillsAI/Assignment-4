from loaders.pdf_loader import PDFLoader
from loaders.docx_loader import DOCXLoader
from loaders.ppt_loader import  PPTLoader
from data_extractor import DataExtractor
from storage import Storage
from storage_sql import StorageSQL
import os
from dotenv import load_dotenv
load_dotenv()

def process_file(loader_class, db_path, base_output_folder):
    """
    Process a file with the specified loader, extracting data and saving it to both a database and the local filesystem.

    Args:
        loader_class: An instance of a file loader (PDFLoader, DOCXLoader, or PPTLoader) initialized with the file path.
        db_path: Path to the SQLite database for storing extracted data.
        base_output_folder: Directory path where extracted data will be saved on the filesystem.
    """
    extractor = DataExtractor(loader_class)

# Get the database config from the environment variables
    db_config = {
    'host': os.getenv('host'),
    'user': os.getenv('user'),
    'password': os.getenv('password'),
    'database': os.getenv('database')
}

    sql_storage = StorageSQL(extractor, db_config)
    
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
    Main function that prompts the user for file paths and initiates the extraction process for each file type.
    """
    db_path = 'extracted_data.db'       # SQLite database file for saving extracted data
    base_output_folder = 'extracted_output'  # Folder where extracted data will be saved

    # Ask user for file paths
    file_paths = input("Enter the file paths (separated by commas): ").split(',')
    
    for file_path in file_paths:
        file_path = file_path.strip()  # Clean up any surrounding spaces

        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}")
            continue
        
        # Determine the file type and assign the appropriate loader
        if file_path.endswith('.pdf'):
            loader = PDFLoader(file_path)
        elif file_path.endswith('.docx'):
            loader = DOCXLoader(file_path)
        elif file_path.endswith('.pptx'):
            loader = PPTLoader(file_path)
        else:
            print(f"Unsupported file format: {file_path}")
            continue
        
        # Process the file
        try:
            process_file(loader, db_path, base_output_folder)
            print(f"Processed file: {file_path}")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

# If the script is executed directly, call the main function to begin processing
if __name__ == "__main__":
    main()
