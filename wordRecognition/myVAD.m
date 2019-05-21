function outputWord = myVAD(inputWordData, energyThreshold, toleranceGap)
%MYVAD Summary of this function goes here
%   Detailed explanation goes here

inputWordEnergy = inputWordData.^2;

mask = false(size(inputWordData));

gapCounter = 1;
for i = 1 : numel(inputWordEnergy)
    if (inputWordEnergy(i) > energyThreshold)
        gapCounter = 1;
        mask(i) = true;
    else
        gapCounter = gapCounter + 1;
        if gapCounter <= toleranceGap
            mask(i) = true;
        end
    end
end

outputWord = inputWordData(mask);
end

