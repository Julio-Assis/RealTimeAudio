function [assignedHiddenStates, accumulatedDist] = myProbDistMeasure(propModelMat, inputMat, distrType)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

if numel(nargin) < 3
    distrType = 'gaussian';
end

S = size(propModelMat, 1);
T = size(inputMat, 1);
D = zeros(S, T);

for s = 1 : S
    for t = 1 : T
        D(s, t) = Inf;
    end
end
D(1, 1) = 0;

for s = 1 : S
   for t = 2 : T
       cost = distance(inputMat(t, :)', propModelMat(s, :, 1)', diag(propModelMat(s, :, 2)), distrType);  %norm(sampleMat(s, :) - inputMat(t, :));
       if s < 2
           D(s, t) = cost + D(s  , t-1);
       elseif s < 3
           D(s, t) = cost + min([D(s  , t-1), ... 
                                D(s-1, t-1)]);
       else
           D(s, t) = cost + min([D(s  , t-1), ... 
                                 D(s-1, t-1), ...
                                 D(s-2, t-1)]);
       end
   end
end
accumulatedDist = D(S, T);

assignedHiddenStates = zeros(T, 1);
assignedHiddenStates(T) = S;

stateDelta = [0, 1, 2]; % 
backStep = 0; % of hidden states
for m = 1 : T-2
    refrStates = [D(S-backStep, T-m), D(S-backStep-1, T-m), D(S-backStep-2, T-m)];
    currentMask = refrStates == min(refrStates);
    if sum(currentMask) > 1
        currentMask = [false, true, false];
    end
    
    backStep = backStep + stateDelta(currentMask);
    minPrevState = S - backStep;

    assignedHiddenStates(T-m) = minPrevState;
end
assignedHiddenStates(1) = 1;

end

%%%%%%%% helper %%%%%%%%
function res = distance(x, mean, CovarMat, type)
    switch type
        case 'gaussian'
            res = 0.5 * ( (x - mean)' * CovarMat^(-1) * (x - mean) ) + log(sqrt(det(2 * pi * CovarMat)));
        case 'laplacian'
            warning('not implemented yet');
            % @todo
            res = 1; 
    end
end

