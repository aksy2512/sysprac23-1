import os
import multiprocessing
import pandas as pd


class EXCEL2TSV:
    def __init__(self, directory: str, header=True) -> None:
        """
        Constructor function
        :param directory: list specifying the path (root folder) of these doc files
        """
        self.directory = directory
        self.batch_convert_to_csv(header)

    def convert_to_csv(self, file_path, header):
        """
        Converts a .docx file to .pdf
        :param file_path: path to the .docx file
        """
        try:
            excelFile = pd.read_excel(file_path)
            excelFile.to_csv(file_path.replace(".xlsx", ".tsv"), sep='\t', index=False, header=header)
            print(f"Successfully converted {file_path} to PDF.")
        except Exception as e:
            print(f"Failed to convert {file_path} to PDF. Error: {e}")

    def batch_convert_to_csv(self, header=True):
        """
        Converts all .docx files in a directory to .pdf
        """
        dir_path = self.directory
        if not os.path.exists(dir_path):
            print(f"Directory path {dir_path} does not exist.")
            return

        pool = multiprocessing.Pool()
        for filename in os.listdir(dir_path):
            if filename.endswith(".xlsx"):
                file_path = os.path.join(dir_path, filename)
                pool.apply_async(self.convert_to_csv, args=(file_path,header,))
        pool.close()
        pool.join()