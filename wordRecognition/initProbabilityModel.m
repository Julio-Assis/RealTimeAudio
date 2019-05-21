function [alignedFeatureVectors, assignedStates, dist] = initProbabilityModel(featureVectors)
%INITPROBABILITYMODEL Summary of this function goes here
%   Detailed explanation goes here


% init variables
numOfStates = 0;
for i = 1 : numel(featureVectors)
    numOfStates = numOfStates + size(featureVectors{i}, 1);
end
numOfStates = round(numOfStates / numel(featureVectors));
numOfFeatureCoeffs = size(featureVectors{1}, 2);
numOfTrainingSamples = numel(featureVectors);

% linear alignment of the given feature vectors
alignedFeatureVectors = cell(size(featureVectors));
for i = 1 : numOfTrainingSamples
    alignedFeatureVectors{i} = myLTW(featureVectors{i}, numOfStates);
end

% init probalistic model
ProbModel = zeros(numOfStates, numOfFeatureCoeffs, 2);

currentMean = zeros(numOfStates, numOfFeatureCoeffs);
currentVar = zeros(numOfStates, numOfFeatureCoeffs);

for i = numel(alignedFeatureVectors)
    currentMean = currentMean + alignedFeatureVectors{i};
end
currentMean = currentMean / numel(alignedFeatureVectors);

for i = numel(alignedFeatureVectors)
    for n = 1 : numOfStates
        for m = 1 : numOfFeatureCoeffs
            currentVar(n, m) = currentVar(n, m) + (alignedFeatureVectors{i}(n, m) - currentMean(n, m))^2;
        end
    end
end
currentVar = currentVar / numel(alignedFeatureVectors);

ProbModel(:, :, 1) = currentMean;
ProbModel(:, :, 2) = 1 * (currentVar + 10e-3);

assignedStates = cell(size(featureVectors));
dist = zeros(1, numel(featureVectors));

for i = 1 : numel(featureVectors)
    [assignedStates{i}, dist(i)] = myProbDistMeasure(ProbModel, featureVectors{i});
end

end

