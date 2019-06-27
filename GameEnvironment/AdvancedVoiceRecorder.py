import sounddevice as sd
import numpy as np
import time
from glob import glob


class AdvancedVoiceRecorder:

    GamesToCommands = {
        'MsPacman-v0': ['UP', 'DOWN', 'LEFT', 'RIGHT', 'SILENCE']
    }

    SavePath = './GameEnvironment/CommandRecords/'

    VADThreshold = 0.05

    def __init__(self, game_name):
        self.game_name = game_name

    def record_commands(self, frames, sample_rate, channels):
        commands = AdvancedVoiceRecorder.GamesToCommands[self.game_name]
        AdvancedVoiceRecorder.display_recording_start(3)
        for command in commands:
            self.record_n_times(command, frames, sample_rate, channels)
        self.play_recorded_commands(sample_rate)

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
            recording = self.discard_first_samples(recording, sample_rate)
            if command != 'SILENCE':
                recording = self.voice_activity_detection(recording, sample_rate)
            file_name = AdvancedVoiceRecorder.SavePath + 'command_{}_record_{}.npy'.format(command, i)
            np.save(file_name, recording)

    def discard_first_samples(self, recording, sample_rate):
        mic_settling_time = 0.125
        num_discarded_samples = np.int(mic_settling_time * sample_rate)
        return recording[num_discarded_samples:]

    @staticmethod
    def voice_activity_detection(recording, sample_rate):
        activated_signal = []
        signal_energy = recording ** 2
        energy_threshold = 0.5
        tolerance_gap = 0.3 * sample_rate
        gap_counter = np.ceil(tolerance_gap / 2)
        for idx in range(signal_energy.size):
            if signal_energy[idx] > energy_threshold:
                activated_signal.append(recording[idx])
                gap_counter = 1
            else:
                gap_counter += 1
                if gap_counter <= tolerance_gap:
                    activated_signal.append(recording[idx])

        return np.array(activated_signal)

    def update_vad_threshold(self):
        rec_silence = self.get_recording_of_command('SILENCE')
        num_of_samples = np.size(rec_silence)
        mean_of_energy = np.sum(rec_silence**2) / num_of_samples
        self.VADThreshold = mean_of_energy

    def get_recording_of_command(self, command):
        all_recordings = glob(self.SavePath + '*')
        for rec in all_recordings:
            if rec.find(command) != -1:
                return np.load(rec)

    def play_recorded_commands(self, sample_rate):
        commands = self.GamesToCommands[self.game_name]
        print('-'*20)
        print('Play back recorded commands...')
        for command in commands:
            rec = self.get_recording_of_command(command)
            sd.play(rec, sample_rate)
            time.sleep(1)

    @staticmethod
    def display_recording_start(seconds_to_wait):
        print('Start recording in...')
        for i in range(seconds_to_wait):
            print(seconds_to_wait - i)
            time.sleep(1)
