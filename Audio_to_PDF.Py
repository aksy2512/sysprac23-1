# Import the convert method from the
import os
import multiprocessing
import speech_recognition as sr
from fpdf import FPDF

class AUD2PDF:
    def __init__(self, directory: str) -> None:
        """
        Constructor function
        :param directory: list specifying the path (root folder) of these doc files
        """
        self.directory = directory
        self.batch_convert_to_pdf()

    def convert_to_pdf(self, file_path):
        """
        Converts .wav file to .pdf file
        :param file_path: path to the  audio files
        """
        try:
            #audio to text
            text=''
            r=sr.Recognizer()
            with sr.AudioFile(file_path) as source:
                audio_data = r.record(source)
                text = r.recognize_google(audio_data)
            pdf = FPDF()  
            
            # Add a page
            pdf.add_page()
            
            # set style and size of font
            # that you want in the pdf
            pdf.set_font("Arial", size = 15)
            
            # insert the texts in pdf
            pdf.cell(200, 10, txt = text, ln = 1, align = 'C')
            
            # save the PDF
            pdf_path = os.path.splitext(file_path)[0] + '.pdf'
            pdf.output(pdf_path)
        
        except Exception as e:

            print(f"Failed to convert {file_path} to pdf. Error: {e}")

    def batch_convert_to_pdf(self):
        """
        Converts all audio files in a directory to .pdf
        """
        dir_path = self.directory
        if not os.path.exists(dir_path):
            print(f"Directory path {dir_path} does not exist.")
            return

        pool = multiprocessing.Pool()
        for filename in os.listdir(dir_path):
            if filename.endswith(".wav"):
                file_path = os.path.join(dir_path, filename)
                pool.apply_async(self.convert_to_pdf, args=(file_path,))
        pool.close()
        pool.join()