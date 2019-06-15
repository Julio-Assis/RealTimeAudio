function [sampleWords_UP, sampleWords_DOWN, sampleWords_LEFT, sampleWords_RIGHT] = readTrainingData()
%READTRAININGDATA Summary of this function goes here
%   Detailed explanation goes here

% total path:
% /home/daniel/Documents/RWTH/rtap/group-b-project/wordRecognition/sampleWords
addpath('sampleWords/up');
sampleWords_UP = cell(1, 13);
sampleWords_UP{1} = audioread('SampleWord_UP_03.wav');
sampleWords_UP{2} = audioread('sampleWord_UP_2019_5_8_15_44.wav');
sampleWords_UP{3} = audioread('sampleWord_UP_2019_5_8_15_45_59.078773.wav');
sampleWords_UP{4} = audioread('sampleWord_UP_2019_5_8_15_46_30.358709.wav');
sampleWords_UP{5} = audioread('sampleWord_UP_2019_5_8_15_47_2.196858.wav');
sampleWords_UP{6} = audioread('sampleWord_UP_2019_5_28_16_5_15.wav');
sampleWords_UP{7} = audioread('sampleWord_UP_2019_5_28_16_6_42.wav');
sampleWords_UP{8} = audioread('sampleWord_UP_2019_5_28_16_9_57.wav');
sampleWords_UP{9} = audioread('sampleWord_UP_2019_5_28_16_10_34.wav');
sampleWords_UP{10} = audioread('sampleWord_UP_2019_5_28_16_12_19.wav');
sampleWords_UP{11} = audioread('sampleWord_UP_2019_5_28_16_13_5.wav');
sampleWords_UP{12} = audioread('sampleWord_UP_2019_5_28_16_13_36.wav');
sampleWords_UP{13} = audioread('sampleWord_UP_2019_5_28_17_1_23.wav');

addpath('sampleWords/down');
sampleWords_DOWN = cell(1, 13);
sampleWords_DOWN{1} = audioread('SampleWord_DOWN_03.wav');
sampleWords_DOWN{2} = audioread('sampleWord_DOWN_2019_5_8_15_44.wav');
sampleWords_DOWN{3} = audioread('sampleWord_DOWN_2019_5_8_15_45_59.078773.wav');
sampleWords_DOWN{4} = audioread('sampleWord_DOWN_2019_5_8_15_46_30.358709.wav');
sampleWords_DOWN{5} = audioread('sampleWord_DOWN_2019_5_8_15_47_2.196858.wav');
sampleWords_DOWN{6} = audioread('sampleWord_DOWN_2019_5_28_16_5_15.wav');
sampleWords_DOWN{7} = audioread('sampleWord_DOWN_2019_5_28_16_6_42.wav');
sampleWords_DOWN{8} = audioread('sampleWord_DOWN_2019_5_28_16_9_57.wav');
sampleWords_DOWN{9} = audioread('sampleWord_DOWN_2019_5_28_16_10_34.wav');
sampleWords_DOWN{10} = audioread('sampleWord_DOWN_2019_5_28_16_12_19.wav');
sampleWords_DOWN{11} = audioread('sampleWord_DOWN_2019_5_28_16_13_5.wav');
sampleWords_DOWN{12} = audioread('sampleWord_DOWN_2019_5_28_16_13_36.wav');
sampleWords_DOWN{13} = audioread('sampleWord_DOWN_2019_5_28_17_1_23.wav');

addpath('sampleWords/left');
sampleWords_LEFT = cell(1, 13);
sampleWords_LEFT{1} = audioread('sampleWord_LEFT_2019_5_8_15_44.wav');
sampleWords_LEFT{2} = audioread('sampleWord_LEFT_2019_5_8_15_45_59.078773.wav');
sampleWords_LEFT{3} = audioread('sampleWord_LEFT_2019_5_8_15_46_30.358709.wav');
sampleWords_LEFT{4} = audioread('sampleWord_LEFT_2019_5_8_15_47_2.196858.wav');
sampleWords_LEFT{5} = audioread('SampleWord_LEFT_03.wav');
sampleWords_LEFT{6} = audioread('sampleWord_LEFT_2019_5_28_15_15_45.wav');
sampleWords_LEFT{7} = audioread('sampleWord_LEFT_2019_5_28_16_5_15.wav');
sampleWords_LEFT{8} = audioread('sampleWord_LEFT_2019_5_28_16_6_42.wav');
sampleWords_LEFT{9} = audioread('sampleWord_LEFT_2019_5_28_16_7_48.wav');
sampleWords_LEFT{10} = audioread('sampleWord_LEFT_2019_5_28_16_9_57.wav');
sampleWords_LEFT{11} = audioread('sampleWord_LEFT_2019_5_28_16_12_19.wav');
sampleWords_LEFT{12} = audioread('sampleWord_LEFT_2019_5_28_16_13_5.wav');
sampleWords_LEFT{13} = audioread('sampleWord_LEFT_2019_5_28_16_13_36.wav');

addpath('sampleWords/right');
sampleWords_RIGHT = cell(1, 13);
sampleWords_RIGHT{1} = audioread('sampleWord_RIGHT_2019_5_8_15_44.wav');
sampleWords_RIGHT{2} = audioread('sampleWord_RIGHT_2019_5_8_15_45_59.078773.wav');
sampleWords_RIGHT{3} = audioread('sampleWord_RIGHT_2019_5_8_15_46_30.358709.wav');
sampleWords_RIGHT{4} = audioread('sampleWord_RIGHT_2019_5_8_15_47_2.196858.wav');
sampleWords_RIGHT{5} = audioread('SampleWord_RIGHT_03.wav');
sampleWords_RIGHT{6} = audioread('sampleWord_RIGHT_2019_5_28_16_6_42.wav');
sampleWords_RIGHT{7} = audioread('sampleWord_RIGHT_2019_5_28_16_7_48.wav');
sampleWords_RIGHT{8} = audioread('sampleWord_RIGHT_2019_5_28_16_9_57.wav');
sampleWords_RIGHT{9} = audioread('sampleWord_RIGHT_2019_5_28_16_10_34.wav');
sampleWords_RIGHT{10} = audioread('sampleWord_RIGHT_2019_5_28_16_12_19.wav');
sampleWords_RIGHT{11} = audioread('sampleWord_RIGHT_2019_5_28_16_13_5.wav');
sampleWords_RIGHT{12} = audioread('sampleWord_RIGHT_2019_5_28_16_13_36.wav');
sampleWords_RIGHT{13} = audioread('sampleWord_RIGHT_2019_5_28_17_1_23.wav');

end

