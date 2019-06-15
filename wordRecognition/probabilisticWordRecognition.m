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

[sampleWords_UP, sampleWords_DOWN, sampleWords_LEFT, sampleWords_RIGHT] = readTrainingData();

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

featureVectors_RIGHT = cell(size(sampleWords_RIGHT));
for i = 1 : length(featureVectors_RIGHT)
    featureVectors_RIGHT{i} = featureExtractrion(sampleWords_RIGHT{i}, fs);
end


%% Train probability model using EM iteration algorithm

% init model
[alignedFeatureVectors_UP, assignedStates_UP, distMeasure] = initProbabilityModel(featureVectors_UP);

errorEps = 1; % set value for converged error

i = 1;
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
    distMeasure = sum(dist_UP)
    i = i + 1;
end

    
