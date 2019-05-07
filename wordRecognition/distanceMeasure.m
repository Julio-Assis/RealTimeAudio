function res = distanceMeasure(labelFeatures, inputAudioFeatures)
%DISTANCEMEASURE Summary of this function goes here
%   Detailed explanation goes here

dist = zeros(1, numel(labelFeatures));


        dist(i) = dist(i) + myDTW(labelFeatures{i}, inputAudioFeatures{i});
    %end
end
res = sum(dist);

end

