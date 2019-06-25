import numpy as np
from glob import glob
from python_speech_features import mfcc


class FeatureExtractor:
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
        mfcc_from_audio = mfcc(array, samplerate=16000)
        normalized_coeffs = self.get_normalized_mfcc(mfcc_from_audio)
        extended_feature_vectors = self.get_mfcc_with_time_derivatives(normalized_coeffs)
        return extended_feature_vectors

    def get_normalized_mfcc(self, coeff_matrix):
        num_of_time_windows = coeff_matrix.shape[0]
        mean_over_time = np.sum(coeff_matrix, 0) / num_of_time_windows
        normalized_coeffs = coeff_matrix - mean_over_time
        energy_peek = np.max(normalized_coeffs[:, 0])
        normalized_coeffs[:, 0] = normalized_coeffs[:, 0] - energy_peek
        return normalized_coeffs

    def get_mfcc_with_time_derivatives(self, coeff_matrix):
        first_derivative = coeff_matrix[1:, :] - coeff_matrix[:-1, :]
        second_derivative = coeff_matrix[2:, :] - 2*coeff_matrix[1:-1, :] + coeff_matrix[:-2, :]
        extended_coeff_matrix = np.concatenate((coeff_matrix[:-2], first_derivative[:-1], second_derivative), axis=1)
        return extended_coeff_matrix

    def save_features(self, array, command):
        file_name = FeatureExtractor.SavePath + command + '.npy'
        np.save(file_name, array)
