function alignedVector = myLTW(inputMat, newMatLength)
%MYLTW Summary of this function goes here
%   Detailed explanation goes here

alignedVector = zeros(newMatLength, size(inputMat, 2));
lenRatio = newMatLength / size(inputMat, 1);

% compRatio = [1, 2, 3, 1/2, 1/3, 2/3, 4/3, 5/3, 7/3, 1/4, 3/4, 5/4, 7/4, 9/4, 1/5, 2/5, 3/5, 4/5, 6/5, 7/5, 8/5, 9/5, 11/5, 1/7, 2/7, 3/7, 4/7, 5/7, 6/7, 8/7, 9/7, 10/7, 11/4];
% diff =      [0, 1, 2,   1,   2,   1,   1,   2,   4,   3,   1,   1,   3,   5,   4,   3,   2,   1,   1,   2,   3,   4,    6,   6,   5,   4,   3,   2,   1,   1,   2,    3,    4];
% 
% mask = abs(compRatio - lenRatio) == min(abs(compRatio - lenRatio));
% c = compRatio(mask);
% d = diff(mask);

r = rats(lenRatio, 3);
c = str2num(r);
d = abs(str2num(r(2)) - str2num(r(end)));

if c < 1
    k = 0;
    for j = 1 : newMatLength
        k = k + 1;
        if mod(k * c, 1) == 0 && k > 1 && size(inputMat, 1) - k - d > newMatLength - j
            k = k + d; % skip d time windows
        end
        alignedVector(j, :) = inputMat(k, :);
    end

elseif c > 1
    k = 0;
    for j = 1 : newMatLength
        k = k + 1;
        alignedVector(j, :) = inputMat(k, :);
        if mod(j * c, 1) == 0 && k > d
            k = k - d;
        end          
    end
else
    for j = 1 : newMatLength
        alignedVector(j, :) = inputMat(j, :);
    end
end

end

