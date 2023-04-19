# Import the convert method from the
import os
import multiprocessing
from docx2pdf import convert

class DOCX2PDF:
    def __init__(self, directory: str) -> None:
        """
        Constructor function
        :param directory: list specifying the path (root folder) of these doc files
        """
        self.directory = directory
        self.batch_convert_to_pdf()

    def convert_to_pdf(self, file_path):
        """
        Converts a .docx file to .pdf
        :param file_path: path to the .docx file
        """
        try:
            convert(file_path)
            print(f"Successfully converted {file_path} to PDF.")
        except Exception as e:
            print(f"Failed to convert {file_path} to PDF. Error: {e}")

    def batch_convert_to_pdf(self):
        """
        Converts all .docx files in a directory to .pdf
        """
        dir_path = self.directory
        if not os.path.exists(dir_path):
            print(f"Directory path {dir_path} does not exist.")
            return

        pool = multiprocessing.Pool()
        for filename in os.listdir(dir_path):
            if filename.endswith(".docx"):
                file_path = os.path.join(dir_path, filename)
                pool.apply_async(self.convert_to_pdf, args=(file_path,))
        pool.close()
        pool.join()

