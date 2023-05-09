# Import the convert method from the
import os
import multiprocessing
import pdfplumber
from docx import Document


class PDF_to_DOCX:
    def __init__(self, directory: tuple) -> None:
        """
        Constructor function
        :param directory: list specifying the path (root folder) of these doc files
        """
        self.directory = directory
        self.convert_to_docx(directory[1])

    def convert_to_docx(self, filename):
        """
        Converts a .pdf file to .docx
        :param file_path: path to the .pdf file
        """
        file_path = 'uploads/' + filename
        try:
            # Open the PDF file
            with pdfplumber.open(file_path) as pdf_file:

                # Create a new Word document
                doc = Document()

                # Loop through each page of the PDF file
                for page in pdf_file.pages:

                # Extract the text from the page
                    text = page.extract_text()

                # Add the text to the Word document
                    doc.add_paragraph(text)

                # Save the Word document
                doc_path = "converted/"+os.path.splitext(filename)[0] + '.docx'
                doc.save(doc_path)

                print(f"Successfully converted {file_path} to DOCX.")
        
        finally : pass

    def batch_convert_to_docx(self):
        """
        Converts all .pdf files in a directory to .docx
        """
        dir_path = self.directory
        if not os.path.exists(dir_path):
            print(f"Directory path {dir_path} does not exist.")
            return

        pool = multiprocessing.Pool()
        for filename in os.listdir(dir_path):
            if filename.endswith(".pdf"):
                file_path = os.path.join(dir_path, filename)
                pool.apply_async(self.convert_to_docx, args=(file_path,))
        pool.close()
        pool.join()