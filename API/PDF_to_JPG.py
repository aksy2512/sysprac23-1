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
        self.convert_to_image(directory)

    def convert_to_image(self, filename):
        """
        Converts a .docx file to .pdf
        :param file_path: path to the .docx file
        """
        file_path = 'uploads/' + filename[1]
        try:
            images = convert_from_path(file_path)
            for i, image in enumerate(images):
                if image.mode != "RGBA" and filename[3].lower() == "png":
                    image = image.convert("RGBA")
                if image.mode != "RGB" and filename[3].lower() == "jpg":
                    image = image.convert("RGB")
                output_filename = os.path.splitext(filename[1])[0]+'.'+filename[3].lower()
                print(filename, output_filename)
                image.save(f'converted/{output_filename}')
                # outname = 'converted/'+os.path.splitext(filename)[0]
                # # converts only first page 
                # image.save(f"{outname}.jpg", "jpeg")
            print(f"Successfully converted {file_path} to jpg.")
        finally : pass

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