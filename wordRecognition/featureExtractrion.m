function features = featureExtractrion(audioInputVector, fs)
%FEATUREEXTRACTRION Summary of this function goes here
%   Detailed explanation goes here

% Mel frequency cepstral coefficients with first and second derivatives
[coeffs, ~, ~] = mfcc(audioInputVector, fs, 'WindowLength', 0.010*fs, 'OverlapLength', 0.005*fs);

% normalization
coeffs_mean = repmat(sum(coeffs, 1) ./ size(coeffs, 1), size(coeffs, 1), 1);
coeffs_norm = coeffs - coeffs_mean;
coeffs_norm(:, 1) = coeffs_norm(:, 1) - max(coeffs_norm(:, 1));

deltaMFCCs = coeffs_norm(2:end, :) - coeffs_norm(1:end-1, :);
deltaDeltaMFCCs = deltaMFCCs(2:end, :) - deltaMFCCs(1:end-1, :);

features = [coeffs_norm(1:end-2, :), deltaMFCCs(1:end-1, :), deltaDeltaMFCCs];

end

