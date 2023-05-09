# Import the convert method from the
import os
import multiprocessing
import speech_recognition as sr
from fpdf import FPDF
from pydub import AudioSegment


class Audio_to_PDF:
    def __init__(self, directory: tuple) -> None:
        """
        Constructor function
        :param directory: list specifying the path (root folder) of these doc files
        """
        self.directory = directory
        self.convert_to_pdf(directory[1])


    def convert_to_pdf(self, filename):
        """
        Converts .wav or .mp3file to .pdf file
        :param file_path: path to the  audio files
        """
        file_path = 'uploads/' + filename
        try:
            # audio to text
            text = ""
            if filename.endswith(".mp3"):
                # create an AudioSegment object from the input file
                aud = AudioSegment.from_file(file_path)
                # export the AudioSegment object as a .wav file
                print(out_path)
                out_path= os.path.splitext(file_path)[0]+'.wav' 
                aud.export(out_path, format="wav")
                r = sr.Recognizer()
                with sr.AudioFile(out_path) as source:
                    audio_data = r.record(source)
                    text = r.recognize_google(audio_data)

            if filename.endswith(".wav"):
                r = sr.Recognizer()
                with sr.AudioFile(file_path) as source:
                    audio_data = r.record(source)
                    text = r.recognize_google(audio_data)

            pdf = FPDF()

            # Add a page
            pdf.add_page()

            # set style and size of font
            # that you want in the pdf
            pdf.set_font("Arial", size=15)

            # insert the texts in pdf
            pdf.cell(200, 10, txt=text, ln=1, align="C")

            # save the PDF
            pdf_path = 'converted/'+os.path.splitext(filename)[0] + ".pdf"
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
            if filename.endswith(".wav") or filename.endswith(".mp3"):
                file_path = os.path.join(dir_path, filename)
                pool.apply_async(self.convert_to_pdf, args=(file_path, filename))
        pool.close()
        pool.join()