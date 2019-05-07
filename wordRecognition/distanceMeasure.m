function res = distanceMeasure(labelFeatures, inputAudioFeatures)
%DISTANCEMEASURE Summary of this function goes here
%   Detailed explanation goes here

assert(numel(labelFeatures) == numel(inputAudioFeatures));
assert(isa(labelFeatures, 'cell') && isa(inputAudioFeatures, 'cell'));

dist = zeros(1, numel(labelFeatures));

for i = 1 : numel(labelFeatures)
    %for k = 1 : size(labelFeatures{i}, 2)
        dist(i) = dist(i) + myDTW(labelFeatures{i}, inputAudioFeatures{i});
    %end
end
res = sum(dist);

end

