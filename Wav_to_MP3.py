# Import the convert method from the
import os
import multiprocessing
from pydub import AudioSegment


class WAV2MP3:
    def __init__(self, directory: str) -> None:
        """
        Constructor function
        :param directory: list specifying the path (root folder) of these doc files
        """
        self.directory = directory
        self.batch_convert_to_mp3()

    def convert_to_mp3(self, file_path, filename):
        """
        Converts .mp3 file to .mp3 file
        :param file_path: path to the  audio files
        """
        try:
                # create an AudioSegment object from the input file
                aud = AudioSegment.from_file(file_path)
                # export the AudioSegment object as a .mp3 file
                out_path = os.path.splitext(file_path)[0] + ".mp3"
                aud.export(out_path, format="mp3")


        except Exception as e:
            print(f"Failed to convert {file_path} to mp3. Error: {e}")

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