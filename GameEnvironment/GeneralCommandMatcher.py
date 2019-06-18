from abc import ABC, abstractmethod

class GeneralCommandMatcher(ABC):

    def __init__(self, frames, sample_rate, channels):
        super().__init__()
        self.frames = frames
        self.sample_rate = sample_rate
        self.channels = channels

    @abstractmethod
    def get_closest(self, command_signal):
        pass
