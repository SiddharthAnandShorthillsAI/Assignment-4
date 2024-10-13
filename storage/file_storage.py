# import csv
# from .storage import Storage

# class FileStorage(Storage):
#     def store(self):
#         # Save text to a file
#         with open('extracted_text.txt', 'w') as text_file:
#             text_file.write(self.extractor.extract_text())

#         # Save tables to a CSV file
#         with open('extracted_tables.csv', 'w', newline='') as csvfile:
#             writer = csv.writer(csvfile)
#             tables = self.extractor.extract_tables()
#             for table in tables:
#                 for row in table:
#                     if isinstance(row, (list, tuple)):
#                         cleaned_row = [cell.strip() for cell in row if isinstance(cell, str) and cell.strip()]  # Remove empty strings
#                         writer.writerow(cleaned_row)
#                     else:
#                         print(f"Unexpected row format: {row}")  # Log unexpected row format

#         # Save images as filenames (simulate saving)
#         images = self.extractor.extract_images()
#         print(f"Images saved: {images}")


# import os
# import csv
# from .storage import Storage
# from PIL import Image
# from io import BytesIO

# class FileStorage(Storage):
#     def __init__(self, extractor, output_dir='output'):
#         """Initialize with an extractor and output directory."""
#         self.extractor = extractor
#         self.output_dir = output_dir

#         # Create the output directory if it doesn't exist
#         if not os.path.exists(self.output_dir):
#             os.makedirs(self.output_dir)

#     def store(self):
#         # Save text to a file
#         text_file_path = os.path.join(self.output_dir, 'extracted_text.txt')
#         with open(text_file_path, 'w') as text_file:
#             text_file.write(self.extractor.extract_text())
#         print(f"Text saved to {text_file_path}")

#         # Save tables to a CSV file
#         tables_file_path = os.path.join(self.output_dir, 'extracted_tables.csv')
#         with open(tables_file_path, 'w', newline='') as csvfile:
#             writer = csv.writer(csvfile)
#             tables = self.extractor.extract_tables()
#             for table in tables:
#                 for row in table:
#                     writer.writerow(row)
#         print(f"Tables saved to {tables_file_path}")

#         # Save hyperlinks to a text file
#         links_file_path = os.path.join(self.output_dir, 'extracted_hyperlinks.txt')
#         with open(links_file_path, 'w') as link_file:
#             links = self.extractor.extract_links()
#             for link in links:
#                 link_file.write(link + '\n')
#         print(f"Hyperlinks saved to {links_file_path}")

#         # Save images in JPG format
#         images_output_dir = os.path.join(self.output_dir, 'images')
#         if not os.path.exists(images_output_dir):
#             os.makedirs(images_output_dir)

#         images = self.extractor.extract_images(images_output_dir)
#         for image in images:
#             print(f"Image saved: {image}")
import os
import csv
from .storage import Storage

class FileStorage(Storage):
    def __init__(self, extractor, output_dir='output'):
        """Initialize with an extractor and output directory."""
        self.extractor = extractor
        self.output_dir = output_dir

        # Create the output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def store(self):
        # Save text to a file
        text_file_path = os.path.join(self.output_dir, 'extracted_text.txt')
        with open(text_file_path, 'w') as text_file:
            text_file.write(self.extractor.extract_text())
        print(f"Text saved to {text_file_path}")

        # Save tables to a CSV file
        tables_file_path = os.path.join(self.output_dir, 'extracted_tables.csv')
        with open(tables_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            tables = self.extractor.extract_tables()
            for table in tables:
                for row in table:
                    writer.writerow(row)
        print(f"Tables saved to {tables_file_path}")

        # Save hyperlinks to a text file
        links_file_path = os.path.join(self.output_dir, 'extracted_hyperlinks.txt')
        with open(links_file_path, 'w') as link_file:
            links = self.extractor.extract_links()
            for link in links:
                link_file.write(link + '\n')
        print(f"Hyperlinks saved to {links_file_path}")

        # Save images in JPG format
        # images_output_dir = 'output/images'  # Directory where images will be saved

        # images_output_dir = os.path.join(self.output_dir, 'images')
        # if not os.path.exists(images_output_dir):
        #     os.makedirs(images_output_dir)

        # images = self.extractor.extract_images(images_output_dir)
        # for image in images:
        #     print(f"Image saved: {image}")
        images_output_dir = 'output/images'  # Directory where images will be saved
        if not os.path.exists(images_output_dir):
            os.makedirs(images_output_dir)  # Create directory if it doesn't exist

        # Extract and save images
        extracted_images = self.extractor.extract_images(images_output_dir)
        if extracted_images is not None:  # Ensure we don't try to iterate over None
            for img in extracted_images:
                print(f"Image saved: {img}")
        else:
            print("No images were extracted.")