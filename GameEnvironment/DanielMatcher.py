import numpy as np
from GameEnvironment.MFCCFeatureExtractor import MFCCFeatureExtractor
from GameEnvironment.GeneralCommandMatcher import GeneralCommandMatcher
from GameEnvironment.AdvancedVoiceRecorder import AdvancedVoiceRecorder


class DanielMatcher(GeneralCommandMatcher):

    def __init__(self, frames, sample_rate, channels, command_files):
        super().__init__(frames, sample_rate, channels)
        self.command_files = command_files
        self.feature_vectors_by_command = {}
        self.load_commands()
        self.feature_extractor = MFCCFeatureExtractor(
            commands=['UP', 'DOWN', 'LEFT', 'RIGHT', 'SILENCE'],
            command_records_path='./GameEnvironment/CommandRecords/'
        )

    def load_commands(self):
        for command_file in self.command_files:
            command_features = np.load(command_file)
            file_name = command_file.split('/')[-1] # get only the last part of the path
            command = file_name.split('.')[0] # remove the file extension
            self.feature_vectors_by_command[command] = command_features

    def get_closest(self, target_signal):
        input_signal = AdvancedVoiceRecorder.voice_activity_detection(target_signal, self.sample_rate)
        closest_command = 'SILENCE'

        if self.considered_as_silence(input_signal):
            return closest_command

        input_features = self.feature_extractor.get_feature_vectors(input_signal)
        min_dist = np.inf
        for command in self.feature_vectors_by_command.keys():
            reference_features = self.feature_vectors_by_command[command]
            dist = self.get_dist_from_dyn_time_warping(input_features, reference_features)

            if dist < min_dist:
                min_dist = dist
                closest_command = command

        return closest_command

    def considered_as_silence(self, signal):
        signal_length = signal.size
        duration_of_signal = signal_length / self.sample_rate
        if duration_of_signal < 0.5:
            return True

        return False

    def get_dist_from_dyn_time_warping(self, input_features, reference_features):
        dist_matrix = self.dynamic_time_warping(input_features, reference_features)

        return dist_matrix[-1, -1]

    def dynamic_time_warping(self, input_features, reference_features):
        init_matrix = self.init_dist_matrix(input_features, reference_features)
        dist_matrix = self.fill_dist_matrix(init_matrix, input_features, reference_features)

        return dist_matrix

    def init_dist_matrix(self, input_features, reference_features):
        reference_time_steps = np.size(reference_features, 0)
        input_time_steps = np.size(input_features, 0)

        matrix_dim = (reference_time_steps, input_time_steps)
        dist_matrix = np.full(matrix_dim, np.inf)
        dist_matrix[0, 0] = 0

        return dist_matrix

    def fill_dist_matrix(self, dist_matrix, input_features, reference_features):
        reference_time_steps = np.size(reference_features, 0)
        input_time_steps = np.size(input_features, 0)

        for refr_time_idx in range(reference_time_steps):
            for input_time_idx in range(1, input_time_steps):
                cost = np.linalg.norm(input_features[input_time_idx] - reference_features[refr_time_idx])
                min_prev_dist = self.get_min_prev_dist(dist_matrix, refr_time_idx, input_time_idx)
                dist_matrix[refr_time_idx, input_time_idx] = cost + min_prev_dist

        return dist_matrix

    def get_min_prev_dist(self, dist_matrix, refr_time_idx, input_time_idx):
        if refr_time_idx < 1:
            min_prev_dist = dist_matrix[refr_time_idx, input_time_idx - 1]
        elif refr_time_idx < 2:
            min_prev_dist = np.min([dist_matrix[refr_time_idx, input_time_idx - 1],
                                    dist_matrix[refr_time_idx - 1, input_time_idx - 1]])
        else:
            min_prev_dist = np.min([dist_matrix[refr_time_idx, input_time_idx - 1],
                                    dist_matrix[refr_time_idx - 1, input_time_idx - 1],
                                    dist_matrix[refr_time_idx - 2, input_time_idx - 1]])

        return min_prev_dist

    def ranked_distances(self, target_signal):
        distances = []
        target_fft = np.fft.fft(target_signal)
        for command in self.feature_vectors_by_command:
            diff = target_fft - self.feature_vectors_by_command[command]
            dist = np.linalg.norm(diff)

            distances.append([command, dist])

        return sorted(distances, key=lambda x: x[1])
