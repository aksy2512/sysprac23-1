import os
import multiprocessing
import pandas as pd


class XLSX_to_CSV:
    def __init__(self, directory: tuple, header=True) -> None:
        """
        Constructor function
        :param directory: list specifying the path (root folder) of these doc files
        """
        self.directory = directory
        self.convert_to_csv(directory[1],header)

    def convert_to_csv(self, filename, header):
        """
        Converts a .docx file to .pdf
        :param file_path: path to the .docx file
        """
        file_path = 'uploads/' + filename
        try:
            excelFile = pd.read_excel(file_path)
            outpath = 'converted/'+os.path.splitext(filename)[0]+'.csv'
            excelFile.to_csv(outpath, index=None, header=header)
            print(f"Successfully converted {file_path} to PDF.")
        finally : pass

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