# Import the convert method from the
import os
import multiprocessing
from pydub import AudioSegment


class MP3_to_WAV:
    def __init__(self, directory: tuple) -> None:
        """
        Constructor function
        :param directory: list specifying the path (root folder) of these doc files
        """
        self.directory = directory
        self.convert_to_wav(directory[1])

    def convert_to_wav(self, filename):
        """
        Converts .mp3 file to .wav file
        :param file_path: path to the  audio files
        """
        file_path = 'uploads/' + filename
        try:
                # create an AudioSegment object from the input file
                aud = AudioSegment.from_file(file_path)
                # export the AudioSegment object as a .wav file
                out_path = 'converted/'+os.path.splitext(filename)[0] + ".wav"
                aud.export(out_path, format="wav")

        finally : pass

    def batch_convert_to_wav(self):
        """
        Converts all audio files in a directory to .wav
        """
        dir_path = self.directory
        if not os.path.exists(dir_path):
            print(f"Directory path {dir_path} does not exist.")
            return

        pool = multiprocessing.Pool()
        for filename in os.listdir(dir_path):
            if filename.endswith(".mp3"):
                file_path = os.path.join(dir_path, filename)
                pool.apply_async(self.convert_to_wav, args=(file_path, filename))
        pool.close()
        pool.join()