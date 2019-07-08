import numpy as np
from python_speech_features import mfcc
from GameEnvironment.FeatureVectors import FeatureVectors
from GameEnvironment.GeneralCommandMatcher import GeneralCommandMatcher

class MartinsMatcher(GeneralCommandMatcher):

    def __init__(self, frames, sample_rate, channels, command_files):
        super().__init__(frames, sample_rate, channels)
        self.vectors = FeatureVectors()
        self.sample_size = frames
        self.frames = []
        self.commands_to_dynamic_distances = {}
        self.command_files = command_files
        self.commands_to_feature_vectors = {}
        self.commands_recognized = ('SILENCE', 'SILENCE', 'SILENCE')
        self.load_commands()

    def load_commands(self):
        """
        Loads the list of feature vectors for each command
        """
        for command_file in self.command_files:
            command_sample = np.load(command_file)
            file_name = command_file.split('/')[-1] # get only the last part of the path
            command = file_name.split('_')[1] # get the DOWN from *_DOWN_*
            v = FeatureVectors(seconds_to_next_vector=1)
            number_of_basic_vectors = len(command_sample)//self.sample_size
            for i in range(number_of_basic_vectors):
                basic_vector = extract_basic_vector(command_sample[self.sample_size*i:self.sample_size*(i+1)])
                v.build_feature_vector(basic_vector)
            self.commands_to_feature_vectors[command] = v.get_feature_vectors()
            number_of_feature_vectors = len(self.commands_to_feature_vectors[command])
            self.commands_to_dynamic_distances[command] = [np.inf for i in range(number_of_feature_vectors + 2)]
            self.commands_to_dynamic_distances[command][2] = 0 #Initialization of the matrix, could be any value (not inf)

    def feed(self, samples):
        """
        Input : audio sample
        Builds the according feature vectors
        Apply continuous dynamic time warping
        Set the recognized command
        """
        basic_vector = extract_basic_vector(samples)
        self.vectors.build_feature_vector(basic_vector)
        feature_vector= self.vectors.get_last_feature_vectors()
        if feature_vector is not None:
            current_min_command = 'SILENCE'
            current_min_value = np.inf
            for command in self.commands_to_dynamic_distances.keys():
                new_dynamic_distance = self.generate_new_dynamic_distance(command, feature_vector)
                if new_dynamic_distance[-1] < current_min_value:
                    current_min_value = new_dynamic_distance[-1]
                    current_min_command = command
                self.commands_to_dynamic_distances[command] = new_dynamic_distance
            for command in self.commands_to_dynamic_distances.keys():
                self.commands_to_dynamic_distances[command][1] = current_min_value
            self.add_recognized_commands(current_min_command)

    def generate_new_dynamic_distance(self, command, feature_vector):
        """
        Generates the new continuous dynamic time warping distance column
        Returns the new cost for this command to be ended at this time frame
        """
        matrix_height = len(self.commands_to_feature_vectors[command]) + 2
        new_dynamic_distance = [np.inf for i in range(matrix_height)]
        for s in range(2, matrix_height):
            dist = distance(self.commands_to_feature_vectors[command][s-2], feature_vector)
            new_dynamic_distance[s] = dist + self.get_min_prev_dist(command, s)
        return new_dynamic_distance

    def get_min_prev_dist(self, command, s):
        return min(
            self.commands_to_dynamic_distances[command][s-2],
            self.commands_to_dynamic_distances[command][s-1],
            self.commands_to_dynamic_distances[command][s])

    def get_closest(self, samples):
        """
        Returns the actual recognized command
        """
        self.feed(samples)
        if self.is_same_recognized_command():
            return self.commands_recognized[-1]
        return 'SILENCE'

    def add_recognized_commands(self, command):
        self.commands_recognized = (self.commands_recognized[1], self.commands_recognized[2], command)

    def is_same_recognized_command(self):
        return self.commands_recognized[0] == self.commands_recognized[1] and \
        self.commands_recognized[1] == self.commands_recognized[2]

def extract_basic_vector(samples):
    """
    samples : the list of the audio samples, of length CHUNK_SIZE
    Returns the COEF_NUMBERS first mfcc coefficients
    """
    return mfcc(np.array(samples), samplerate=44100, nfft=2048, numcep=16, appendEnergy=False)[0]

def distance(vector1, vector2):
    """
    Takes 2 numpy arrays of shape (x,) and returns the norm2 of the distance btween them.
    """
    return np.linalg.norm(vector1 - vector2)
