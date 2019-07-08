import numpy as np

class FeatureVectors:
    """
    Class that represents the list of features vectors.
    seconds_to_next_vector :
        It represents the duration in seconds between 2 times frames (usually around 20ms).
        It doesn't influence directly the recognition, so it could be left at 1.
        However, it does influence the distance between 2 feature vectors.
    _basic_vectors :
        It is a list of numpy arrays.
        These arrays are of shape (COEF_NUMBERS,).
        There is one array for each time frame (for each window).
    _accousticVectors :
        It is a list of numpy arrays.
        These arrays are of shape (3*COEF_NUMBERS,).
        There is one array for each frame, except the first and last one.
        The arrays include the COEF_NUMBERS mfcc coefficients (same as in _basic_vectors).
        The COEF_NUMBERS next are the first derivative (central) of the mfcc coefficients.
        The last COEF_NUMBERS are the second derivative (central) of the mfcc coefficients.
    """

    def __init__(self, seconds_to_next_vector=1):
        self._basic_vectors = []
        self._feature_vectors = []
        self.seconds_to_next_vector = seconds_to_next_vector #time between 2 vectors

    def get_feature_vectors(self):
        """
        returns _feature_vectors
        """
        return self._feature_vectors

    def build_feature_vector(self, basic_vector):
        """
        Adds basic_vector to the basic vectors.
        If there are at least 3 arrays in _basic_vectors, then add a new array to _featureVector.
        This added array is composed of the basic vectors and its 2 first central derivatives
        basic_vector must be the array returned by the mfcc.
        """
        basic_vector = basic_vector - np.mean(basic_vector)
        self._basic_vectors.append(basic_vector)
        if len(self._basic_vectors) > 2:
            #if there are at least 3 basic vectors we can calculate the central derivative for the vector before this one
            first_derivative  = (basic_vector - self._basic_vectors[-3])/(2*self.seconds_to_next_vector)
            second_derivative = (basic_vector - 2*self._basic_vectors[-2] + self._basic_vectors[-3])/(self.seconds_to_next_vector**2)
            feature_vector = np.concatenate((basic_vector, first_derivative, second_derivative))
            self._feature_vectors.append(feature_vector)

    def get_last_feature_vectors(self):
        """
        If there is at least an feature vector then returns it, else returns None
        """
        if len(self._feature_vectors):
            return self._feature_vectors[-1]
        return None

    def __len__(self):
        return len(self._feature_vectors)
