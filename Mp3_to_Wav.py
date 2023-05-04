# Import the convert method from the
import os
import multiprocessing
from pydub import AudioSegment


class MP32WAV:
    def __init__(self, directory: str) -> None:
        """
        Constructor function
        :param directory: list specifying the path (root folder) of these doc files
        """
        self.directory = directory
        self.batch_convert_to_wav()

    def convert_to_wav(self, file_path, filename):
        """
        Converts .mp3 file to .wav file
        :param file_path: path to the  audio files
        """
        try:
                # create an AudioSegment object from the input file
                aud = AudioSegment.from_file(file_path)
                # export the AudioSegment object as a .wav file
                out_path = os.path.splitext(file_path)[0] + ".wav"
                aud.export(out_path, format="wav")


        except Exception as e:
            print(f"Failed to convert {file_path} to wav. Error: {e}")

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