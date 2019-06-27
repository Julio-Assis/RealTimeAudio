import sounddevice as sd
import numpy as np
import time

class BasicVoiceRecorder:

    GamesToCommands = {
        'MsPacman-v0': ['UP', 'DOWN', 'LEFT', 'RIGHT', 'SILENCE']
    }

    SavePath = './GameEnvironment/CommandRecords/'

    def __init__(self, game_name):
        self.game_name = game_name

    def record_commands(self, frames, sample_rate, channels):
        commands = BasicVoiceRecorder.GamesToCommands[self.game_name]
        BasicVoiceRecorder.display_recording_start(3)
        for command in commands:
            self.record_n_times(command, frames, sample_rate, channels)

    def record_n_times(self, command, frames, sample_rate, channels, times=1):

        print('-'*20)
        print("Let's record the command={} {} times".format(command, times))
        for i in range(times):
            print('Starting record {}'.format(i + 1))
            print('Speak!')
            recording = sd.rec(
                frames=frames,
                samplerate=sample_rate,
                channels=channels,
                blocking=True
            )
            print('Record {} done'.format(i + 1))
            file_name = BasicVoiceRecorder.SavePath + \
                'command_{}_record_{}.npy'.format(command, i)
            np.save(file_name, recording)

    @staticmethod
    def display_recording_start(seconds_to_wait):
        print('Start recording in...')
        for i in range(seconds_to_wait):
            print(seconds_to_wait - i)
            time.sleep(1)
