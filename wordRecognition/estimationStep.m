function ProbModel = estimationStep(alignedFeatureVectors, assignedStates)
%ESTIMATIONSTEP 
%   alignedFeatureVectors:      cell array of number of training recordings
%                               of the current word. each cell contains a
%                               2D matrix of size: time steps x feature
%                               coefficients
%   assignedStates:             cell array of number of training recordings
%                               of the current word. each cell contains
%                               integer array with length of time steps of
%                               the respective recorded word.
%   ProbModel:                  matrix of size: #states x #feature coeffs x
%                               #params (= 2). first param is mean, second is variance 


% Init varaibles
numOfTrainingSamples = size(alignedFeatureVectors, 2);
numOfStates = size(alignedFeatureVectors{1}, 1);
numOfFeatureCoeffs = size(alignedFeatureVectors{1}, 2);

ProbModel = zeros(numOfStates, numOfFeatureCoeffs, 2);
Container = cell(numOfStates, 1); % one cell for each state of the probability model

% Fill container with assigned states
for i = 1 : numOfTrainingSamples
    for j = 1 : size(assignedStates{i}, 1)
        assignedIdx = assignedStates{i}(j);
        newAssignment = alignedFeatureVectors{i}(assignedIdx, :);
        
        Container{assignedIdx} = cat(1, Container{assignedIdx}, newAssignment);
    end
end

% Compute probability model for every state with assigned time steps
for n = 1 : numOfStates
    if ~isempty(Container{n})
        currentSampleNumber = size(Container{n}, 1);
        currentMean = sum(Container{n}, 1) ./ currentSampleNumber;
        currentVar = sum((Container{n} - currentMean).^2, 1) ./ currentSampleNumber;

        ProbModel(n, :, 1) = currentMean;
        ProbModel(n, :, 2) = 1 * (currentVar + 10e-3);
    else
        if n > 2 % when empty, use average of last two models
            ProbModel(n, :, :) = (ProbModel(n-1, :, :) + ProbModel(n-2, :, :)) ./ 2;
        end
    end
end

end

