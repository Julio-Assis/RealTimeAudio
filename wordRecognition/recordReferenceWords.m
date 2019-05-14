%% init recording
fs = 16000;
nBits = 8;
nChannels = 1;

trashRecording = audiorecorder(fs, nBits, nChannels); % unused recording for catching unwanted sounds at beginning of recording

word_UP_Recording = audiorecorder(fs, nBits, nChannels);
word_DOWN_Recording = audiorecorder(fs, nBits, nChannels);
word_LEFT_Recording = audiorecorder(fs, nBits, nChannels);
word_RIGHT_Recording = audiorecorder(fs, nBits, nChannels);

word_UP_Recording.StartFcn = 'disp(''Speak target word: UP'')';
word_DOWN_Recording.StartFcn   = 'disp(''Speak target word: DOWN'')';
word_LEFT_Recording.StartFcn  = 'disp(''Speak target word: LEFT'')';
word_RIGHT_Recording.StartFcn  = 'disp(''Speak target word: RIGHT'')';

word_UP_Recording.StopFcn  = 'disp(''End of recording.'')';
word_DOWN_Recording.StopFcn    = 'disp(''End of recording.'')';
word_LEFT_Recording.StopFcn   = 'disp(''End of recording.'')';
word_RIGHT_Recording.StopFcn   = 'disp(''End of recording.'')';

%% record words
pause on
record(trashRecording, 1);

disp('Please speak the following target words when asked for:')
disp('UP')
disp('DOWN')
disp('LEFT')
disp('RIGHT')
pause(2);
disp('...Start recording in:')
for i = 1 : 3
    disp(4-i)
    pause(1);
end

record(word_UP_Recording, 2);
pause(3);

record(word_DOWN_Recording, 2);
pause(3);

record(word_LEFT_Recording, 2);
pause(3);

record(word_RIGHT_Recording, 2);
pause(3);

word_UP_data = getaudiodata(word_UP_Recording);
word_DOWN_data = getaudiodata(word_DOWN_Recording);
word_LEFT_data = getaudiodata(word_LEFT_Recording);
word_RIGHT_data = getaudiodata(word_RIGHT_Recording);

%% play recordings
pause(1);
play(word_UP_Recording);
pause(3);
play(word_DOWN_Recording);
pause(3);
play(word_LEFT_Recording);
pause(3);
play(word_RIGHT_Recording);

%% save audio files
% answer = input('Do want to write the audio files for these recordings? (type: y, then Enter to continue)');
% if strcmp(answer, 'y') || strcmp(answer, 'Y')
    %% crop signals to length of active speaking duration
    threshold = 0.05;
    toleranceGap = 0.3 * fs;
    word_UP = myVAD(word_UP_data, threshold, toleranceGap);
    word_DOWN = myVAD(word_DOWN_data, threshold, toleranceGap);
    word_LEFT = myVAD(word_LEFT_data, threshold, toleranceGap);
    word_RIGHT = myVAD(word_RIGHT_data, threshold, toleranceGap);

    %% write audio files
    c = clock; % create time stamp
    c(6) = round(c(6));
    c = string(c);
    c = c(1) + "_" + c(2) + "_" + c(3) + "_" + c(4) + "_" + c(5) + "_" + c(6);

    audiowrite("sampleWords/sampleWord_UP_" + c + ".wav", word_UP, fs);
    audiowrite("sampleWords/sampleWord_DOWN_" + c + ".wav", word_DOWN, fs);
    audiowrite("sampleWords/sampleWord_LEFT_" + c + ".wav", word_LEFT, fs);
    audiowrite("sampleWords/sampleWord_RIGHT_" + c + ".wav", word_RIGHT, fs);

