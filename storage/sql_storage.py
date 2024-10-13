import sqlite3
from .storage import Storage

class SQLStorage(Storage):
    def store(self):
        conn = sqlite3.connect('extracted_data.db')
        cursor = conn.cursor()

        # Create tables for storing text, links, and tables
        cursor.execute('''CREATE TABLE IF NOT EXISTS Text (content TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Links (url TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Images (metadata TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS Tables (content TEXT)''')

        # Insert extracted text into the database
        text = self.extractor.extract_text()
        cursor.execute("INSERT INTO Text (content) VALUES (?)", (text,))
                # Insert extracted links
        links = self.extractor.extract_links()
        for link in links:
            cursor.execute("INSERT INTO Links (url) VALUES (?)", (link,))

        # Insert extracted images (just simulating metadata here)
        images = self.extractor.extract_images()
        for img in images:
            cursor.execute("INSERT INTO Images (metadata) VALUES (?)", (img,))
            
        # Insert extracted tables (as CSV strings)
        tables = self.extractor.extract_tables()
        for table in tables:
            content = ', '.join([' | '.join(map(str, row)) for row in table if isinstance(row, (list, tuple))])
            cursor.execute("INSERT INTO Tables (content) VALUES (?)", (content,))

        conn.commit()
        conn.close()