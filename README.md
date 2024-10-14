This project delivers a modular Python solution for extracting text, hyperlinks, images, and tables from PDF, DOCX, and PPTX files, while also capturing metadata such as file type, page or slide numbers, font styles, and more. <br>
Additionally, it offers functionality to store the extracted data in both local files and a MySQL database.

`Features`
  Text Extraction: Extracts plain text from PDF, DOCX, and PPTX files along with metadata.<br>
  Hyperlink Extraction: Extracts URLs from PDF, DOCX, and PPTX files.<br>
  Image Extraction: Extracts images and metadata (resolution, format, page/slide number) and stores them in separate folders.<br>
  Table Extraction: Extracts tables and stores them in CSV format for each file type.<br>
  Storage Options: File Storage: Saves text, links, images, and tables into separate files.<br>
  SQL Storage: Stores extracted data into a database. <br>


  Installation <br>
1)Clone the repo: <br>
git clone https://github.com/your_username/pdf-docx-pptx-extractor.git <br>
2)Set up a Python virtual environment and install dependencies: <br>
python -m venv env <br>
source env/bin/activate <br>
3)Install the required dependencies and then run the main.py file



