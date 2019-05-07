function [normalizedMFCCs, deltaMFCCs, deltaDeltaMFCCs] = featureExtractrion(audioInputVector, fs)
%FEATUREEXTRACTRION Summary of this function goes here
%   Detailed explanation goes here

% Mel frequency cepstral coefficients with first and second derivatives
[coeffs, ~, ~] = mfcc(audioInputVector, fs);

% % normalization
coeffs_mean = repmat(sum(coeffs, 2) / size(coeffs, 2), 1, size(coeffs, 2));
coeffs_norm = coeffs - coeffs_mean;
coeffs_norm(:, 1) = coeffs_norm(:, 1) - max(coeffs_norm(:, 1));

normalizedMFCCs = coeffs_norm;
deltaMFCCs = normalizedMFCCs(2:end, :) - normalizedMFCCs(1:end-1, :);
deltaDeltaMFCCs = deltaMFCCs(2:end, :) - deltaMFCCs(1:end-1, :);
end

