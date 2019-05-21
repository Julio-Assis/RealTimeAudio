%% init recording
fs = 16000;
nBits = 8;
nChannels = 1;

trashRecording = audiorecorder(fs, nBits, nChannels);
inputWordRecording = audiorecorder(fs, nBits, nChannels);
inputWordRecording.StartFcn = 'disp(''Start speaking  word.'')';
inputWordRecording.StopFcn   = 'disp(''End of recording.'')';

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
energyThreshold = 0.05;
toleranceGap = 0.3 * fs;

inputWord = myVAD(inputWordData, energyThreshold, toleranceGap);
inputWordAudio = audioplayer(inputWord, fs); % for playback

%% % load sample audio vectors

% @todo: implement function: readTrainingData()

addpath('sampleWords');
sampleWords_UP = cell(1, 5);
sampleWords_UP{1} = audioread('sampleWord_UP_2019_5_8_15_44.wav');
sampleWords_UP{2} = audioread('sampleWord_UP_2019_5_8_15_45_59.078773.wav');
sampleWords_UP{3} = audioread('sampleWord_UP_2019_5_8_15_46_30.358709.wav');
sampleWords_UP{4} = audioread('sampleWord_UP_2019_5_8_15_47_2.196858.wav');
sampleWords_UP{5} = audioread('SampleWord_UP_03.wav');

sampleWords_DOWN = cell(1, 5);
sampleWords_DOWN{1} = audioread('sampleWord_DOWN_2019_5_8_15_44.wav');
sampleWords_DOWN{2} = audioread('sampleWord_DOWN_2019_5_8_15_45_59.078773.wav');
sampleWords_DOWN{3} = audioread('sampleWord_DOWN_2019_5_8_15_46_30.358709.wav');
sampleWords_DOWN{4} = audioread('sampleWord_DOWN_2019_5_8_15_47_2.196858.wav');
sampleWords_DOWN{5} = audioread('SampleWord_DOWN_03.wav');

sampleWords_LEFT = cell(1, 5);
sampleWords_LEFT{1} = audioread('sampleWord_LEFT_2019_5_8_15_44.wav');
sampleWords_LEFT{2} = audioread('sampleWord_LEFT_2019_5_8_15_45_59.078773.wav');
sampleWords_LEFT{3} = audioread('sampleWord_LEFT_2019_5_8_15_46_30.358709.wav');
sampleWords_LEFT{4} = audioread('sampleWord_LEFT_2019_5_8_15_47_2.196858.wav');
sampleWords_LEFT{5} = audioread('SampleWord_LEFT_03.wav');

sampleWords_RIGHT = cell(1, 5);
sampleWords_RIGHT{1} = audioread('sampleWord_RIGHT_2019_5_8_15_44.wav');
sampleWords_RIGHT{2} = audioread('sampleWord_RIGHT_2019_5_8_15_45_59.078773.wav');
sampleWords_RIGHT{3} = audioread('sampleWord_RIGHT_2019_5_8_15_46_30.358709.wav');
sampleWords_RIGHT{4} = audioread('sampleWord_RIGHT_2019_5_8_15_47_2.196858.wav');
sampleWords_RIGHT{5} = audioread('SampleWord_RIGHT_03.wav');

%% feature extraction
% Mel frequency cepstral coefficients with first and second derivatives
featureVectors_UP = cell(size(sampleWords_UP));
for i = 1 : length(featureVectors_UP)
    featureVectors_UP{i} = featureExtractrion(sampleWords_UP{i}, fs);
end

featureVectors_DOWN = cell(size(sampleWords_DOWN));
for i = 1 : length(featureVectors_DOWN)
    featureVectors_DOWN{i} = featureExtractrion(sampleWords_DOWN{i}, fs);
end

featureVectors_LEFT = cell(size(sampleWords_LEFT));
for i = 1 : length(featureVectors_LEFT)
    featureVectors_LEFT{i} = featureExtractrion(sampleWords_LEFT{i}, fs);
end
numOfTrainingSamples
featureVectors_RIGHT = cell(size(sampleWords_RIGHT));
for i = 1 : length(featureVectors_RIGHT)
    featureVectors_RIGHT{i} = featureExtractrion(sampleWords_RIGHT{i}, fs);
end


%% Train probability model using EM iteration algorithm

% init model
[alignedFeatureVectors_UP, assignedStates_UP, distMeasure] = initProbabilityModel(featureVectors_UP);

errorEps = 1; % set value for converged error

while(distMeasure > errorEps)
    %% Estimation step
    % call estimation function and create new probablity distributions for
    % hidden states
    ProbModel_UP = estimationStep(alignedFeatureVectors_UP, assignedStates_UP);
    
    %% Maximization step
    % call maximization function and assign feature vectors to most likely
    % states for new evaluation of PDFs
    [assignedStates_UP, dist_UP] = maximizationStep(ProbModel_UP, featureVectors_UP);
    
    %% evaluate distance for abortion criterium
    distMeasure = sum(dist_UP);
end

    
