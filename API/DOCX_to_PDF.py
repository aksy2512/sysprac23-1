# Import the convert method from the
import os
import multiprocessing
from docx2pdf import convert
from app import User, db
import sys
import subprocess

def generate_pdf(doc_path, path):

    subprocess.call(['soffice',
                 '--headless',
                 '--convert-to',
                 'pdf',
                 '--outdir',
                 path,
                 doc_path])
    return doc_path

class DOCX_to_PDF:
    def __init__(self, files) -> None:
        """
        Constructor function
        :param directory: list specifying the path (root folder) of these doc files
        """
        self.files = files
        self.directory = "converted"
        self.dest_format = ".pdf"
        self.batch_convert_to_pdf()


    def convert_to_pdf(self):
        """
        Converts a .docx file to .pdf
        :param file_path: path to the .docx file
        """
        try:
            # file = User.query.filter(User.file_uuid == f.file_uuid).first()
            # # mark status as active
            # file.status = "Active"
            # db.session.commit()
            # print("*"*100)
            # print("Before")
            # print(User.query.all())
            filename = self.files[1]
            file_path = os.path.join('uploads',filename)
            dest_path = os.path.join("converted",filename.split(".")[0]+self.dest_format)
            # print("Destination: ",dest_path)
            # now converting
            print(file_path,dest_path)
            if(sys.platform=='linux'):
                generate_pdf(file_path,"converted/")
            else:
                convert(file_path,dest_path)
            # updating the databse and saving file path
            # file.status = "Done"
            # file.converted_file_path = dest_path
            # db.session.commit()
            # print("*"*20)
            # print("After")
            # print(User.query.all())
            print(f"Successfully converted {file_path} to PDF.")
        except Exception as e:
            print(e)
            print(f"Failed to convert {file_path} to PDF. Error: {e}")

    def batch_convert_to_pdf(self):
        """
        Converts all .docx files in a directory to .pdf
        """
        dir_path = self.directory
        if not os.path.exists(dir_path):
            print(f"Directory path {dir_path} does not exist.")
            return
        if self.files[1].endswith(".docx"):
            self.convert_to_pdf()

