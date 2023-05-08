import os
import multiprocessing
from pdf2image import convert_from_path


class PDF2IMAGE:
    def __init__(self, directory: str) -> None:
        """
        Constructor function
        :param directory: list specifying the path (root folder) of these doc files
        """
        self.directory = directory
        self.batch_convert_to_image()

    def convert_to_image(self, file_path):
        """
        Converts a .docx file to .pdf
        :param file_path: path to the .docx file
        """
        try:
            images = convert_from_path(file_path)
            for i, image in enumerate(images):
                filename = file_path.split('.')[0]
                image.save(f"{filename}_page_{i}.jpg", "JPEG")
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