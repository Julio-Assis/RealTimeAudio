import sounddevice as sd
import numpy as np


class VoiceRecorder:

    GamesToCommands = {
        'MsPacman-v0': ['UP', 'DOWN', 'LEFT', 'RIGHT', 'SILENCE']
    }

    SavePath = './GameEnvironment/CommandRecords/'

    def __init__(self, game_name):
        self.game_name = game_name

    def record_commands(self):
        commands = VoiceRecorder.GamesToCommands[self.game_name]
        for command in commands:
            self.record_n_times(command)

    def record_n_times(self, command, times=1, fs=44100, duration=2, channels=1):

        print('-'*20)
        print("Let's record the command={} {} times".format(command, times))
        for i in range(times):
            print('Starting record {}'.format(i + 1))
            print('Speak!')
            recording = sd.rec(
                int(duration * fs),
                samplerate=fs,
                channels=channels,
                blocking=True
            )
            print('Record {} done'.format(i + 1))
            file_name = VoiceRecorder.SavePath + \
                'command_{}_record_{}.npy'.format(command, i)
            np.save(file_name, recording)
