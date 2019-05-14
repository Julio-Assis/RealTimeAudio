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

featureVectors_RIGHT = cell(size(sampleWords_RIGHT));
for i = 1 : length(featureVectors_RIGHT)
    featureVectors_RIGHT{i} = featureExtractrion(sampleWords_RIGHT{i}, fs);
end

%% training probability model
% init target probability model
meanTimeLength = 0;
for i = 1 : numel(featureVectors_UP)
    meanTimeLength = meanTimeLength + size(featureVectors_UP{i}, 1);
end
meanTimeLength = round(meanTimeLength / numel(featureVectors_UP));
numOfFeatureCoeffs = size(featureVectors_UP{1}, 2);

alignedFeatureVectors_UP = cell(size(featureVectors_UP));
targetFeatureVector_UP = zeros(meanTimeLength, length(featureVectors_UP));

% comp = [1, 2, 3, 1/2, 1/3, 2/3, 4/3, 5/3, 7/3, 1/4, 3/4, 5/4, 7/4, 9/4, 1/5, 2/5, 3/5, 4/5, 6/5, 7/5, 8/5, 9/5, 11/5, 1/7, 2/7, 3/7, 4/7, 5/7, 6/7, 8/7, 9/7, 10/7, 11/4];
% diff = [0, 1, 2,   1,   2,   1,   1,   2,   4,   3,   1,   1,   3,   5,   4,   3,   2,   1,   1,   2,   3,   4,    6,   6,   5,   4,   3,   2,   1,   1,   2,    3,    4];

for i = 1 : length(featureVectors_UP)
    alignedFeatureVectors_UP{i} = myLTW(featureVectors_UP{i}, meanTimeLength);
end


%% init probalistic model
ProbModel = zeros(meanTimeLength, numOfFeatureCoeffs, 2);
% distributionParams = zeros(meanTimeLength, size(alignedFeatureVectors_UP{1}, 2), 2);

currentMean = zeros(meanTimeLength, numOfFeatureCoeffs);
currentVar = zeros(meanTimeLength, numOfFeatureCoeffs);

for i = numel(alignedFeatureVectors_UP)
    currentMean = currentMean + alignedFeatureVectors_UP{i};
end
currentMean = currentMean / numel(alignedFeatureVectors_UP);

for i = numel(alignedFeatureVectors_UP)
    for n = 1 : meanTimeLength
        for m = 1 : numOfFeatureCoeffs
            currentVar(n, m) = currentVar(n, m) + (alignedFeatureVectors_UP{i}(n, m) - currentMean(n, m))^2;
        end
    end
end
currentVar = currentVar / numel(alignedFeatureVectors_UP);

ProbModel(:, :, 1) = currentMean;
ProbModel(:, :, 2) = currentVar;


for i = 1 : numel(featureVectors_UP{i})
    myProbDistMeasure(ProbModel, featureVectors_UP{i});
end


%% EM Interation algorithm

% while(distMeasure > errorEps)
%     %% Estimation step
%     % call estimation function and create new probablity distributions for
%     % hidden states
%     
%     %% Maximization step
%     % call maximization function and assign feature vectors to most likely
%     % states for new evaluation of PDFs
%     
%     % distance measure for abortion criterium
% end

    
