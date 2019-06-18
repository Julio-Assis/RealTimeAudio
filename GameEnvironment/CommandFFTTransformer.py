import numpy as np
from glob import glob


class CommandFFTTransformer:

    SavePath = './GameEnvironment/CommandTransforms/'

    def __init__(self, commands, command_records_path):
        self.commands = commands
        self.command_records_path = command_records_path

    def record_transforms(self):
        files = glob(self.command_records_path + '*')
        print('checking files')
        print(files)
        for f in files:
            sound_array = np.load(f)
            command = self.get_command(f)
            fft = self.calculate_fft(sound_array)
            self.save_fft(fft, command)

    def get_command(self, file):
        for c in self.commands:
            if file.find(c) != -1:
                return c
        raise Exception('There is no file saved for this command')

    def calculate_fft(self, array):
        return np.fft.fft(array)

    def save_fft(self, array, command):
        file_name = CommandFFTTransformer.SavePath + command + '.npy'
        np.save(file_name, array)
