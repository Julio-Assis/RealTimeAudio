import numpy as np


class CommandMatcher:

    def __init__(self, command_files):
        self.command_files = command_files
        self.fft_transforms_by_command = {}
        self.load_commands()

    def load_commands(self):

        for command_file in self.command_files:
            command_fft = np.load(command_file)
            # get only the last part of the path
            file_name = command_file.split('/')[-1]
            command = file_name.split('.')[0]  # remove the file extension
            self.fft_transforms_by_command[command] = command_fft

    def get_closest(self, target_signal):

        target_fft = np.fft.fft(target_signal)
        min_dist = np.inf
        for command in self.fft_transforms_by_command.keys():
            diff = target_fft - self.fft_transforms_by_command[command]
            dist = np.linalg.norm(diff)

            if dist < min_dist:
                min_dist = dist
                closest_command = command

        return closest_command

    def ranked_distances(self, target_signal):
        distances = []
        target_fft = np.fft.fft(target_signal)
        for command in self.fft_transforms_by_command:
            diff = target_fft - self.fft_transforms_by_command[command]
            dist = np.linalg.norm(diff)

            distances.append([command, dist])

        return sorted(distances, key=lambda x: x[1])
