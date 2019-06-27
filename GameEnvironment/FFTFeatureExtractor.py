import numpy as np
from glob import glob


class FFTFeatureExtractor:

    SavePath = './GameEnvironment/CommandFeatures/'

    def __init__(self, commands, command_records_path):
        self.commands = commands
        self.command_records_path = command_records_path

    def extract_features(self):
        files = glob(self.command_records_path + '*')
        for f in files:
            sound_array = np.load(f)
            command = self.get_command(f)
            feature_vectors = self.get_feature_vectors(sound_array)
            self.save_features(feature_vectors, command)

    def get_command(self, file):
        for c in self.commands:
            if file.find(c) != -1:
                return c
        raise Exception('There is no file saved for this command')

    def get_feature_vectors(self, array):
        # implement method to extract your desired features
        return np.fft.fft(array)

    def save_features(self, feature_vectors, command):
        file_name = FFTFeatureExtractor.SavePath + command + '.npy'
        np.save(file_name, feature_vectors)
