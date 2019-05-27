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

CHUNK = 1024 #chunk size
FORMAT = pyaudio.paInt16 #2byte per sample : +-32768
CHANNELS = 2
RATE = 44100 #sampling rate
NFFT=2048 #FFT size
NUMCEP=16 #number of coefficients
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "down.wav"
ENERGY_BEGIN = 11 #to be changed from mic (it's a log scale)
ENERGY_BEGIN_NUMBERS = 2
ENERGY_BEGIN_BEFORE_NUMBERS = 5
ENERGY_END = 9
ENERGY_END_NUMBERS = 5
ACTIVATION_WAIT = 1 #number of seconds to wait after mic activation
format = "%dh"%(CHUNK * CHANNELS) #h for short, so 16bits beacause we use paInt16

class Vectors:
    def __init__(self, period=1):
        self._basicVectors = []
        self._acousticVectors = []
        self.period = period #time between 2 vectors
    
    def getAcousticVectors(self):
        return self._acousticVectors
    
    def addBasicVector(self, v): #central derivative => 1 frame late
        # v = v - meanVector(v)
        self._basicVectors.append(v)
        if len(self._basicVectors) > 2:
            dv  = [(v[i] - self._basicVectors[-3][i])/(2*self.period) for i in range(len(v))]
            ddv = [(v[i] - 2*self._basicVectors[-2][i] + self._basicVectors[-3][i])/(self.period**2) for i in range(len(v))]
            av = numpy.concatenate((v, dv, ddv))
            self._acousticVectors.append(av)
    
    def getLastAcousticVectors(self):
        if len(self._acousticVectors):
            return self._acousticVectors[-1], True
        return None, False
        
    def __len__(self):
        return len(self._acousticVectors)
            
def meanVector(v, ignoreFirst=True):
    return numpy.mean(v[ignoreFirst:])

def extractVectorsFromFile(file_path):
    vectors = Vectors()
    numbersAfterBegin = 0
    wf = wave.open(file_path, 'rb')
    p = pyaudio.PyAudio()
    data = wf.readframes(CHUNK)
    while data != b'':
        t = struct.unpack(format, data)
        m = extractVector(t[::2])
        vectors.addBasicVector(m)
        data = wf.readframes(CHUNK)
    p.terminate()
    wf.close()
    return vectors.getAcousticVectors()

def extractVector(t):
    return mfcc(numpy.array(t), samplerate=RATE, nfft=NFFT, numcep=NUMCEP, appendEnergy=False)[0]

def getEnergy(t):
    return mfcc(numpy.array(t), samplerate=RATE, nfft=NFFT, numcep=1, appendEnergy=True)[0][0]

def listWavFiles():
    f = []
    files = os.listdir(os.path.dirname(os.path.realpath(__file__)))
    for file in files:
        if ".wav" in file:
            f.append(file)
    return f

def getWords():
    words = dict()
    files = listWavFiles()
    for file in files:
        words[file.split(".")[0]] = extractVectorsFromFile(file)
    return words

def compare(input, words):
    m = "Error"
    d_min = math.inf
    for word in words.keys():
        d = distance.dynamicDistance(words[word], input)
        print(word, d)
        if d < d_min:
            d_min = d
            m = word
    return m

def test():
    d = getWords()
    p = pyaudio.PyAudio()
    matrixes = {}
    for word in d.keys():
        matrixes[word] = numpy.full((len(d[word]) + 2, 1), numpy.inf)
        matrixes[word][2, 0] = 0
        
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=1,
                    frames_per_buffer=CHUNK)
    
    vectors = Vectors()
    waitAfterActivation(stream)
    print("* recording")
    
    frames = []
    
    numbersAfterBegin = 0
    old_min_value = numpy.inf
    wordsRecognized = []
    f = True
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)): #number of chunks
        data = stream.read(CHUNK)
        frames.append(data)
        t = struct.unpack(format, data) #unpacks the bytes in an array of size CHUNK * CHANNELS (interleaved !)
        m = extractVector(t[::2])
        # if numbersAfterBegin >= ENERGY_BEGIN_NUMBERS or m[0] >= ENERGY_BEGIN:
        #     numbersAfterBegin += 1
        vectors.addBasicVector(m)
        m, e = vectors.getLastAcousticVectors()
        if e:
            # print("---")
            current_min = "None"
            current_min_value = numpy.inf
            for word in d.keys():
                x = len(d[word]) + 2
                matrixes[word] = numpy.concatenate((matrixes[word], numpy.full((x, 1), numpy.inf)), axis=1)
                for s in range(2, x):
                    dis = distance.distance(d[word][s-2], m)
                    if f:
                        f = False
                        print(word, dis)
                    matrixes[word][s, -1] = dis + min(matrixes[word][s-2, -2], matrixes[word][s-1, -2], matrixes[word][s, -2])
                if matrixes[word][-1, -1] < current_min_value:
                    current_min_value = matrixes[word][-1, -1]
                    current_min = word
                # print(word, matrixes[word][-1, -1])
            old_min_value = current_min_value
            # matrixes[word][1, -1] = old_min_value
            wordsRecognized.append(current_min)
            print(current_min, current_min_value)
        # elif m[0] < ENERGY_BEGIN:
        #     numbersAfterBegin = 0
        #     vectors = Vectors()
    print(compare(vectors.getAcousticVectors(), d))
    if not numbersAfterBegin:
        print("Try again louder")
    
    print("* done recording")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    return matrixes, vectors

def record(file_name):
    numbersAfterBegin = 0
    numbersAfterEnd = 0
            
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=1,
                    frames_per_buffer=CHUNK)
    waitAfterActivation(stream)
    print("* recording")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)): #number of chunks
        data = stream.read(CHUNK)
        t = struct.unpack(format, data)
        m = extractVector(t[::2])
        e = getEnergy(t[::2])
        if numbersAfterEnd < ENERGY_END_NUMBERS:
            if (numbersAfterBegin >= ENERGY_BEGIN_NUMBERS or e >= ENERGY_BEGIN):
                if numbersAfterBegin == ENERGY_BEGIN_NUMBERS:
                    a = max(0, len(frames) - ENERGY_BEGIN_NUMBERS - ENERGY_BEGIN_BEFORE_NUMBERS)
                    frames = frames[a:]
                if m[0] >= ENERGY_BEGIN:
                    numbersAfterBegin += 1
                    numbersAfterEnd = 0
                else: #numbersAfterBegin >= ENERGY_BEGIN_NUMBERS
                    numbersAfterEnd += 1
                frames.append(data)
            elif (numbersAfterBegin < ENERGY_BEGIN_NUMBERS and e < ENERGY_BEGIN):
                numbersAfterBegin = 0
    print("* done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(file_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def recordNoise(file_name, duration=RECORD_SECONDS): #should probably be pretty small, will try this next time
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=1,
                    frames_per_buffer=CHUNK)
    waitAfterActivation(stream)
    print("* recording")
    frames = []
    for i in range(0, int(RATE / CHUNK * duration)): #number of chunks
        data = stream.read(CHUNK)
        frames.append(data)
    print("* done recording")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(file_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def energyPlot():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=1,
                    frames_per_buffer=CHUNK)
    e = []
    waitAfterActivation(stream)
    print("* recording")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)): #number of chunks
        data = stream.read(CHUNK)
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
    print("Recording in", ACTIVATION_WAIT)
    t = time.time()
    while (time.time() - t) < ACTIVATION_WAIT:
        stream.read(CHUNK)