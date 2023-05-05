# Import the convert method from the
import os
import multiprocessing
from docx2pdf import convert
from app import User, db

class DOCX2PDF:
    def __init__(self, files: list) -> None:
        """
        Constructor function
        :param directory: list specifying the path (root folder) of these doc files
        """
        self.files = files
        self.directory = "converted"
        self.dest_format = ".pdf"
        self.batch_convert_to_pdf()

    def convert_to_pdf(self, f):
        """
        Converts a .docx file to .pdf
        :param file_path: path to the .docx file
        """
        try:
            file = User.query.filter(User.file_uuid == f.file_uuid).first()
            # mark status as active
            file.status = "Active"
            db.session.commit()
            print("*"*100)
            print("Before")
            print(User.query.all())
            file_path = f.path
            dest_path = os.path.join("converted",file.name.split(".")[0]+self.dest_format)
            print(dest_path)
            # now converting
            convert(file_path,dest_path)
            # updating the databse and saving file path
            file.status = "Done"
            file.converted_file_path = dest_path
            db.session.commit()
            print("*"*20)
            print("After")
            print(User.query.all())
            print(f"Successfully converted {file_path} to PDF.")
        except Exception as e:
            print(e)
            print("FUCKKKKK "*100)
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
        for f in self.files:
            if f.name.endswith(".docx"):
                pool.apply_async(self.convert_to_pdf, args=(f,))
        pool.close()
        pool.join()

