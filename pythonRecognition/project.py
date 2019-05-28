import pyaudio
import wave
import struct
import time
import numpy
import math
import distance
import os
import pylab
from python_speech_features import mfcc
from python_speech_features import fbank

"""
To run :
install python-speech-features, PyAudio and numpy if needed (through pip install python-speech-features)
execute this in a shell
record several words through record("up.wav")
lauch test() afterward
"""


"""
TODO:
RETAKE samples
REWORK stille calculator (mean of 10 sec ?/several different frame noise1, noise2, ... ?)
"""

CHUNK_SIZE = 1024 #chunk size
FORMAT = pyaudio.paInt16 #2byte per sample : +-32768
CHANNELS = 2
SAMPLING_RATE = 44100 #sampling rate
FFT_SIZE=2048 #fast fourier size size
COEF_NUMBERS=16 #number of coefficients
RECORD_SECONDS = 5
ENERGY_THRESHOLD_BEGIN = 12 #to be changed from mic (it's a log scale)
ENERGY_THRESHOLD_BEGIN_NUMBERS = 2 #numbers of frame where the energy must exceed the ENERGY_THRESHOLD_BEGIN
ENERGY_THRESHOLD_BEFORE_BEGIN_NUMBERS = 5 #numbers of frame that are added just before the threshold_begin is exceeded
ENERGY_THRESHOLD_END = 10
ENERGY_THRESHOLD_END_NUMBERS = 5
ACTIVATION_WAIT = 1 #number of seconds to wait after mic activation
format = "%dh"%(CHUNK_SIZE * CHANNELS) #h for short, so 16bits because we use paInt16

class Vectors:
    """
    Class that represents the acoustic features vectors.
    period :
        It represents the duration in seconds between 2 times frames (ie 1/SAMPLING_RATE).
        It doesn't influence the recognition, so it may be left at 1.
    _basicVectors :
        It is a list of numpy arrays.
        These arrays are of shape (COEF_NUMBERS,).
        There is one array for each time frame.
    _accousticVectors :
        It is a list of numpy arrays.
        These arrays are of shape (3*COEF_NUMBERS,).
        There is one array for each frame, except the first and last one.
        The arrays include the COEF_NUMBERS mfcc coefficients (same as in _basicVectors).
        The COEF_NUMBERS next are the first derivative (central) of the mfcc coefficients.
        The last COEF_NUMBERS are the second derivative (central) of the mfcc coefficients.

    getAcousticVecetors():
        returns _acousticVectors

    addBasicVector(v):
        add v to _basicVectors.
        If there are at least 3 arrays in _basicVectors, then add a new array to _acousticVectors

    getLastAccousticVectors():
        If there is at least an acoustic vector then returns (the last acoustic vector, True)
        Else returns (None, False)
    """

    def __init__(self, period=1):
        self._basicVectors = []
        self._acousticVectors = []
        self.period = period #time between 2 vectors
    
    def getAcousticVectors(self):
        return self._acousticVectors
    
    def addBasicVector(self, basicVector): #central derivative => 1 frame late
        """
        Adds basicVector to the basic vectors and possibly its derivative to acoustic vectors.
        basicVector must be the array returned by the mfcc.
        """
        basicVector = basicVector - numpy.mean(basicVector)
        self._basicVectors.append(basicVector)
        if len(self._basicVectors) > 2: #if there are at least 3 basic vectors we can calculate the derivative
            dBasicVector  = (basicVector - self._basicVectors[-3])/(2*self.period) #first derivative
            ddBasicVector = (basicVector - 2*self._basicVectors[-2] + self._basicVectors[-3])/(self.period**2) #second derivative
            acousticBasicVector = numpy.concatenate((basicVector, dBasicVector, ddBasicVector))
            self._acousticVectors.append(acousticBasicVector)
    
    def getLastAcousticVectors(self):
        if len(self._acousticVectors):
            return self._acousticVectors[-1], True
        return None, False
        
    def __len__(self):
        return len(self._acousticVectors)
            
def meanVector(v, ignoreFirst=False):
    return numpy.mean(v[ignoreFirst:])

def extractVectorsFromFile(filePath):
    """
    filePath : The path to the file to read.
    Returns a list which contains the acoustic vectors of the audio file.
    """
    vectors = Vectors()
    wf = wave.open(filePath, 'rb')
    p = pyaudio.PyAudio()
    data = wf.readframes(CHUNK_SIZE)
    while data != b'':
        samples = struct.unpack(format, data)
        basicVector = extractVector(samples[::2]) #samples[::2] because the samples are interleaved
        vectors.addBasicVector(basicVector)
        data = wf.readframes(CHUNK_SIZE)
    p.terminate()
    wf.close()
    return vectors.getAcousticVectors()

def extractVector(samples):
    """
    samples : the list of the audio samples, of length CHUNK_SIZE
    Returns the COEF_NUMBERS first mfcc coefficients
    """
    return mfcc(numpy.array(samples), samplerate=SAMPLING_RATE, nfft=FFT_SIZE, numcep=COEF_NUMBERS, appendEnergy=False)[0]

def getEnergy(samples):
    """
    samples : the list of the audio samples, of length CHUNK_SIZE
    Returns the energy of samples
    """
    return mfcc(numpy.array(samples), samplerate=SAMPLING_RATE, nfft=FFT_SIZE, numcep=1, appendEnergy=True)[0][0]

def listWavFiles():
    """
    Returns the list of the names of the .wav files that are in the same folder as this file.
    """
    filesNameList = []
    files = os.listdir(os.path.dirname(os.path.realpath(__file__)))
    for file in files:
        if ".wav" in file: #if it has a .wav extension
            filesNameList.append(file)
    return filesNameList

def getWords():
    """
    Returns a dictionnary d.
    The keys of d are the name of the files (without extension, ie without .wav).
    The values are lists containing the acoustic vectors of the related file.
    """
    words = dict()
    files = listWavFiles()
    for fileName in files:
        words[fileName.split(".")[0]] = extractVectorsFromFile(fileName)
    return words

def compare(input, words):
    """
    input: The list of the acoustic vectors of the recorded audio.
    words : A dictionnary (string, [acoustic vector]) for example generated by getWords()
    Returns the word minimizing the dynamic distance between its acoustic vectors and the input
    Prints (word, distance) for each word.
    """
    minimumWord = "Error"
    minimumDistance = math.inf
    for word in words.keys():
        dist = distance.dynamicDistance(words[word], input)
        print(word, dist)
        if dist < minimumDistance:
            minimumDistance = dist
            minimumWord = word
    return minimumWord

def test():
    """
    Records an audio signal and try to recognize the words being spoken in real time.
    Returns matrixes, vectors.
        matrixes : dictionnary (string word, numpy.array matrix).
            word : the string of the word. For example "up", "left", ...
            matrix : the matrix generated by the 0,1,2 way
        vectors : A Vectors object representing the recorded audio

    Prints (word currently being recognized, distance from the model to the audio) for each time frame.
    Prints what is printed by compare()
    Prints the result of compare (not real time).
    """
    wordsDictionnary = getWords()
    p = pyaudio.PyAudio()
    matrixes = {}
    for word in wordsDictionnary.keys():
        matrixes[word] = numpy.full((len(wordsDictionnary[word]) + 2, 1), numpy.inf)
        matrixes[word][2, 0] = 0
        
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLING_RATE,
                    input=True,
                    input_device_index=1,
                    frames_per_buffer=CHUNK_SIZE)
    
    vectors = Vectors()
    waitAfterActivation(stream)
    print("* recording")
    
    frames = []
    
    numbersAfterBegin = 0
    oldMinValue = numpy.inf
    wordsRecognized = []
    energyThresholdAttained = False
    
    for i in range(0, int(SAMPLING_RATE / CHUNK_SIZE * RECORD_SECONDS)): #number of chunks
        data = stream.read(CHUNK_SIZE)
        frames.append(data)
        samples = struct.unpack(format, data) #unpacks the bytes in an array of size CHUNK_SIZE * CHANNELS (interleaved !)
        basicVector = extractVector(samples[::2])
        if energyThresholdAttained or getEnergy(samples[::2]) >= ENERGY_THRESHOLD_BEGIN:
            energyThresholdAttained = True
            vectors.addBasicVector(basicVector)
            acousticVector, e = vectors.getLastAcousticVectors()
            if e:
                # print("---")
                currentMin = "None"
                currentMinValue = numpy.inf
                for word in wordsDictionnary.keys():
                    x = len(wordsDictionnary[word]) + 2
                    matrixes[word] = numpy.concatenate((matrixes[word], numpy.full((x, 1), numpy.inf)), axis=1)
                    for s in range(2, x):
                        dis = distance.distance(wordsDictionnary[word][s-2], acousticVector)
                        matrixes[word][s, -1] = dis + min(
                            matrixes[word][s-2, -2],
                            matrixes[word][s-1, -2],
                            matrixes[word][s, -2])
                    if matrixes[word][-1, -1] < currentMinValue:
                        currentMinValue = matrixes[word][-1, -1]
                        currentMin = word
                    # print(word, matrixes[word][-1, -1])
                oldMinValue = currentMinValue
                # matrixes[word][1, -1] = oldMinValue
                wordsRecognized.append(currentMin)
                print(currentMin, currentMinValue)
    print(compare(vectors.getAcousticVectors(), wordsDictionnary))
    if not numbersAfterBegin:
        print("Try again louder")
    
    print("* done recording")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    return matrixes, vectors

def record(fileName):
    """
    Record audio and save it to a file.
    There is an energy threshold.
    fileName : The name of the audio file where the recorded audio will be saved. (ex: "up.wav")
    """
    numbersAfterBegin = 0
    numbersAfterEnd = 0
            
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLING_RATE,
                    input=True,
                    input_device_index=1,
                    frames_per_buffer=CHUNK_SIZE)
    waitAfterActivation(stream)
    print("* recording")
    frames = []
    for i in range(0, int(SAMPLING_RATE / CHUNK_SIZE * RECORD_SECONDS)): #number of chunks
        data = stream.read(CHUNK_SIZE)
        samples = struct.unpack(format, data)
        energy = getEnergy(samples[::2])
        if numbersAfterEnd < ENERGY_THRESHOLD_END_NUMBERS:
            #if we didn't stop recording
            if (numbersAfterBegin >= ENERGY_THRESHOLD_BEGIN_NUMBERS or energy >= ENERGY_THRESHOLD_BEGIN):
                #if we started recording
                if numbersAfterBegin == ENERGY_THRESHOLD_BEGIN_NUMBERS:
                    #if we just successfully passed the threshold enough times
                    #we need to record the future, but also the ENERGY_THRESHOLD_BEGIN_NUMBERS frames before
                    framesBegin = max(0, len(frames) - ENERGY_THRESHOLD_BEGIN_NUMBERS - ENERGY_THRESHOLD_BEFORE_BEGIN_NUMBERS)
                    frames = frames[framesBegin:] #we start the recording with the ENERGY_THRESHOLD_BEGIN_NUMBERS last frames
                if energy >= ENERGY_THRESHOLD_BEGIN:
                    #if we pass the threshold, we won't stop recording for ENERGY_THRESHOLD_END_NUMBERS frames
                    numbersAfterBegin += 1
                    numbersAfterEnd = 0
                else: #numbersAfterBegin >= ENERGY_THRESHOLD_BEGIN_NUMBERS
                    #if we don't pass the threshold, we need to know if we didn't pass it since a long time
                    numbersAfterEnd += 1
                frames.append(data)
            elif (numbersAfterBegin < ENERGY_THRESHOLD_BEGIN_NUMBERS and energy < ENERGY_THRESHOLD_BEGIN):
                #if we didn't start recording and the energy isn't high enough, we restart the counter
                numbersAfterBegin = 0
    print("* done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(fileName, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(SAMPLING_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def recordNoise(fileName, duration=RECORD_SECONDS): #should probably be pretty small, will try this next time
    """
    Records audio and save it to a file.
    Doesn't use energy threshold => use it for noise recording.
    fileName : The name of the audio file where the recorded audio will be saved. (ex: "noise.wav")
    duration : The duration of the recording.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLING_RATE,
                    input=True,
                    input_device_index=1,
                    frames_per_buffer=CHUNK_SIZE)
    waitAfterActivation(stream)
    print("* recording")
    frames = []
    for i in range(0, int(SAMPLING_RATE / CHUNK_SIZE * duration)): #number of chunks
        data = stream.read(CHUNK_SIZE)
        frames.append(data)
    print("* done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(fileName, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(SAMPLING_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def energyPlot():
    """
    Plots the energy of the different frames.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLING_RATE,
                    input=True,
                    input_device_index=1,
                    frames_per_buffer=CHUNK_SIZE)
    e = []
    waitAfterActivation(stream)
    print("* recording")
    frames = []
    for i in range(0, int(SAMPLING_RATE / CHUNK_SIZE * RECORD_SECONDS)): #number of chunks
        data = stream.read(CHUNK_SIZE)
        t = struct.unpack(format, data)
        m = getEnergy(t[::2])
        e.append(m)
    print("* done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()
    pylab.plot(e)
    pylab.show()

def waitAfterActivation(stream):
    """
    Utility function that is used to allow the mics to get online.
    stream : The stream to read from.
    """
    print("Recording in", ACTIVATION_WAIT)
    t = time.time()
    while (time.time() - t) < ACTIVATION_WAIT:
        stream.read(CHUNK_SIZE)
