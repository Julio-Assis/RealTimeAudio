function [assignedStates, dist] = maximizationStep(ProbModel, featureVectors)
%MAXIMIZATIONSTEP Summary of this function goes here
%   Detailed explanation goes here

assignedStates = cell(size(featureVectors));
dist = zeros(1, numel(featureVectors));

for i = 1 : numel(featureVectors)
    [assignedStates{i}, dist(i)] = myProbDistMeasure(ProbModel, featureVectors{i});
end

end

