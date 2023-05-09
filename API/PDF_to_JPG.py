import os
import multiprocessing
from pdf2image import convert_from_path


class PDF_to_JPG:
    def __init__(self, directory: tuple) -> None:
        """
        Constructor function
        :param directory: list specifying the path (root folder) of these doc files
        """
        self.directory = directory
        self.convert_to_image(directory[1])

    def convert_to_image(self, filename):
        """
        Converts a .docx file to .pdf
        :param file_path: path to the .docx file
        """
        file_path = 'uploads/' + filename
        try:
            images = convert_from_path(file_path)
            for i, image in enumerate(images):
                outname = 'converted/'+filename.split('.')[0]
                image.save(f"{outname}_page_{i}.jpg", "JPG")
            print(f"Successfully converted {file_path} to PDF.")
        except Exception as e:
            print(f"Failed to convert {file_path} to PDF. Error: {e}")

    def batch_convert_to_image(self):
        """
        Converts all .docx files in a directory to .pdf
        """
        dir_path = self.directory
        if not os.path.exists(dir_path):
            print(f"Directory path {dir_path} does not exist.")
            return

        pool = multiprocessing.Pool()
        for filename in os.listdir(dir_path):
            if filename.endswith(".pdf"):
                file_path = os.path.join(dir_path, filename)
                pool.apply_async(self.convert_to_image, args=(file_path,))
        pool.close()
        pool.join()