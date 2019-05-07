%% init recording
fs = 16000;
nBits = 8;
nChannels = 1;

trashRecording = audiorecorder(fs, nBits, nChannels);
inputWordRecording = audiorecorder(fs, nBits, nChannels);
inputWordRecording.StartFcn = 'disp(''Start speaking  word.'')';
inputWordRecording.StopFcn   = 'disp(''End of recording.'')';

% load target audio vectors
sampleWordUP = audioread('SampleWord_UP_03.wav');
sampleWordDOWN = audioread('SampleWord_DOWN_03.wav');
sampleWordLEFT = audioread('SampleWord_LEFT_03.wav');
sampleWordRIGHT = audioread('SampleWord_RIGHT_03.wav');

%% record word
pause on
record(trashRecording, 1);

disp('Speak one of the following target words:')
disp('UP')
disp('DOWN')
disp('LEFT')
disp('RIGHT')
pause(2);
disp('...Start recording in:')
for i = 1 : 3
    disp(4-i)
    pause(1);
end

record(inputWordRecording, 2);
pause(3);

inputWordData = getaudiodata(inputWordRecording);

%% play recordings
play(inputWordRecording);
pause(3);

%% apply voice activation by thresholding
inputWordEnergy = inputWordData.^2;

VAD_mask = false(size(inputWordData));

energyThreshold = 0.05;
toleranceGap = 0.3 * fs;
gapCounter = 1;
for i = 1 : numel(inputWordEnergy)
    if (inputWordEnergy(i) > energyThreshold)
        gapCounter = 1;
        VAD_mask(i) = true;
    else
        gapCounter = gapCounter + 1;
        if gapCounter <= toleranceGap
            VAD_mask(i) = true;
        end
    end
end

inputWord = inputWordData(VAD_mask);
VAD_inputWord_audio = audioplayer(inputWord, fs);

%% feature extraction
% Mel frequency cepstral coefficients with first and second derivatives
featureVector_UP    = featureExtractrion(sampleWordUP, fs);
featureVector_DOWN  = featureExtractrion(sampleWordDOWN, fs);
featureVector_LEFT  = featureExtractrion(sampleWordLEFT, fs);
featureVector_RIGHT = featureExtractrion(sampleWordRIGHT, fs);
featureVector_Input = featureExtractrion(inputWord, fs);

%% DTW on feature vector sequence
dist_UP = myDTW(featureVector_UP, featureVector_Input);
dist_DOWN = myDTW(featureVector_DOWN, featureVector_Input);
dist_LEFT = myDTW(featureVector_LEFT, featureVector_Input);
dist_RIGHT = myDTW(featureVector_RIGHT, featureVector_Input);

%% disp result
disp('Recognized word: ')
switch min( [dist_UP, dist_DOWN, dist_LEFT, dist_RIGHT] )
    case dist_UP
        disp('UP')
    case dist_DOWN
        disp('DOWN')
    case dist_LEFT
        disp('LEFT')
    case dist_RIGHT
        disp('RIGHT')
end



