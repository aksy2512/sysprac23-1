# Import the convert method from the
import os
import multiprocessing
from pydub import AudioSegment


class WAV_to_MP3:
    def __init__(self, directory: str) -> None:
        """
        Constructor function
        :param directory: list specifying the path (root folder) of these doc files
        """
        self.directory = directory
        self.convert_to_mp3(directory[1])

    def convert_to_mp3(self, filename):
        """
        Converts .mp3 file to .mp3 file
        :param file_path: path to the  audio files
        """
        file_path = 'uploads/' + filename
        try:
                # create an AudioSegment object from the input file
                aud = AudioSegment.from_file(file_path)
                # export the AudioSegment object as a .mp3 file
                out_path = 'converted/'+os.path.splitext(filename)[0] + ".mp3"
                aud.export(out_path, format="mp3")


        finally : pass

    def batch_convert_to_mp3(self):
        """
        Converts all audio files in a directory to .mp3
        """
        dir_path = self.directory
        if not os.path.exists(dir_path):
            print(f"Directory path {dir_path} does not exist.")
            return

        pool = multiprocessing.Pool()
        for filename in os.listdir(dir_path):
            if filename.endswith(".wav"):
                file_path = os.path.join(dir_path, filename)
                pool.apply_async(self.convert_to_mp3, args=(file_path, filename))
        pool.close()
        pool.join()