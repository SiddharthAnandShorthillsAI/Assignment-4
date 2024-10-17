import os
import csv
import sqlite3
from io import BytesIO
import mysql.connector
from PIL import Image
from data_extractor import DataExtractor
from loaders.pdf_loader import PDFLoader
from loaders.docx_loader import DOCXLoader
from loaders.ppt_loader import PPTLoader
from storage.storage import Storage
class StorageSQL:
    def __init__(self, extractor: DataExtractor, db_config):
        self.extractor = extractor
        self.db_config = db_config

        # First connect to MySQL without specifying a database to create it if needed
        self.conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        
        self._create_database_if_not_exists(db_config['database'])  # Ensure the database exists
        self.conn.database = db_config['database']  # Set the database for the connection

        # db_config is a dictionary containing MySQL connection parameters
        self.conn = mysql.connector.connect(**db_config)
        self.create_tables()

    def _create_database_if_not_exists(self, database_name):
        """Create the database if it does not already exist."""
        cursor = self.conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        cursor.close()
        print(f"Database '{database_name}' checked/created successfully.")
  
    def create_tables(self):
        """Create tables in the MySQL database if they don't exist."""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS extracted_text (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_type VARCHAR(255),
                content TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS extracted_links (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_type VARCHAR(255),
                link TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS extracted_images (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_type VARCHAR(255),
                image LONGBLOB
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS extracted_tables (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_type VARCHAR(255),
                table_data TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS extracted_metadata (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_type VARCHAR(255),
                `key` VARCHAR(255),
                `value` TEXT
            )
        ''')
        self.conn.commit()

    def save_text(self):
        self._save_to_db('extracted_text', 'content', self.extractor.extract_text)

    def save_links(self):
        self._save_to_db('extracted_links', 'link', lambda: self.extractor.extract_links(), is_link=True)

    def save_images(self):
        images = self.extractor.extract_images()
        file_type = self._get_file_type()

        cursor = self.conn.cursor()
        for idx, image_data in enumerate(images):
            try:
                image_data = self._prepare_image_data(image_data)
                img_byte_arr = self._get_image_bytes(image_data)

                cursor.execute('''
                    INSERT INTO extracted_images (file_type, image)
                    VALUES (%s, %s)
                ''', (file_type, img_byte_arr))

            except Exception as e:
                print(f"Error saving image {idx + 1}: {e}")

        self.conn.commit()
        print("Image data saved to database.")

    def save_metadata(self):
        metadata = self.extractor.extract_metadata()
        file_type = self._get_file_type()
        cursor = self.conn.cursor()

        for key, value in metadata.items():
            cursor.execute('''
                INSERT INTO extracted_metadata (file_type, `key`, `value`)
                VALUES (%s, %s, %s)
            ''', (file_type, key, value))

        self.conn.commit()
        print("Metadata saved to database.")

    def _save_to_db(self, table_name, column_name, extract_func, is_link=False):
        """General method to save data to the database."""
        data = extract_func()
        file_type = self._get_file_type()

        cursor = self.conn.cursor()
        for item in data:
            if is_link and isinstance(item, tuple):
                item = item[1]  # Only save the hyperlink part
            cursor.execute(f'''
                INSERT INTO {table_name} (file_type, {column_name})
                VALUES (%s, %s)
            ''', (file_type, item))

        self.conn.commit()
        print(f"{column_name.capitalize()} data saved to database.")

    def save_tables(self):
        tables = self.extractor.extract_tables()
        file_type = self._get_file_type()

        cursor = self.conn.cursor()
        for idx, table in enumerate(tables):
            # Convert None to empty string in the table data
            table_data = '\n'.join([','.join(str(item) if item is not None else '' for item in row) for row in table])

            cursor.execute('''
                INSERT INTO extracted_tables (file_type, table_data)
                VALUES (%s, %s)
            ''', (file_type, table_data))

        self.conn.commit()
        print("Table data saved to database.")

    def _get_image_bytes(self, image_data):
        """Convert image data to binary format for storage."""
        img_byte_arr = BytesIO()
        image = Image.open(image_data)
        image.save(img_byte_arr, format=image.format)
        return img_byte_arr.getvalue()

    def _prepare_image_data(self, image_data):
        """Prepare image data for saving."""
        if isinstance(image_data, dict):  # For pdfplumber images
            return BytesIO(image_data['stream'].get_data())
        elif isinstance(image_data, bytes):  # For DOCX/PPT images
            return BytesIO(image_data)
        return image_data  # Handle any unexpected cases

    def _get_file_type(self):
        """Helper method to get the file type (pdf, docx, ppt) based on the loader class."""
        file_loader_mapping = {
            PDFLoader: 'pdf',
            DOCXLoader: 'docx',
            PPTLoader: 'ppt'
        }

        for loader_class, file_type in file_loader_mapping.items():
            if isinstance(self.extractor.file_loader, loader_class):
                return file_type
        
        return 'unknown'

    def close(self):
        """Close the database connection."""
        self.conn.close()