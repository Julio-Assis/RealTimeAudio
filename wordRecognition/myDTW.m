function accumulatedDist = myDTW(sampleMat, inputMat)
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

S = size(sampleMat, 1);
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
       cost = norm(sampleMat(s, :) - inputMat(t, :));
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
end

