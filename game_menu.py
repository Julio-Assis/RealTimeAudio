from GameEnvironment.GameEnvironment import GameEnvironment
from GameEnvironment.DumbMatcher import DumbMatcher
from GameEnvironment.DanielMatcher import DanielMatcher
from GameEnvironment.MartinsMatcher import MartinsMatcher
from GameEnvironment.FFTFeatureExtractor import FFTFeatureExtractor
from GameEnvironment.MFCCFeatureExtractor import MFCCFeatureExtractor
from GameEnvironment.AdvancedVoiceRecorder import AdvancedVoiceRecorder
from GameEnvironment.BasicVoiceRecorder import BasicVoiceRecorder
from glob import glob
import sys

def get_inputs_and_play(game_name):

    greeting_message()
    game_mode = get_game_mode()
    game_mode = validate_game_mode(game_mode)
    execute_game_mode(game_name, game_mode)

def greeting_message():
    print('Welcome to the voiced PacMan Game!')
    print("It's a pleasure to have you playing with us")
    print('')
    print('-'*25)

def get_game_mode():
    print('Please choose one of the available game modes or press any other key to leave')
    print('1. Random playing')
    print('2. Controlling by arrows')
    print('3. DumbMatcher')
    print('4. MartinMatcher') # Replace with the appropriate names of your matcher
    print('5. DanielMatcher') # once you have implemented them
    print('0. To leave the game')
    mode = input()
    return mode

def validate_game_mode(game_mode):

    bye_message = 'Bye bye =D see you next time'
    try:
        game_mode = int(game_mode)
    except:
        print(bye_message)
        sys.exit()

    if game_mode in [1, 2, 3, 4, 5]:
        return game_mode

    print(bye_message)
    sys.exit()

def execute_game_mode(game_name, game_mode):

    if game_mode == 1:
        play_random(game_name)
    elif game_mode == 2:
        play_with_keys(game_name)
    elif game_mode == 3:
        play_with_dumb_matcher(game_name)
    elif game_mode == 4:
        play_with_martins_matcher(game_name)
    elif game_mode == 5:
        play_with_daniel_matcher(game_name)
    else:
        print('Bye bye')
        sys.exit()

def play_random(game_name):
    sample_rate = 44100
    frames = 2 * sample_rate
    channels = 1

    game = GameEnvironment(game_name, frames, sample_rate, channels)
    game.run_game(mode=game.play_random)

def play_with_keys(game_name):
    sample_rate = 44100
    frames = 2 * sample_rate
    channels = 1

    game = GameEnvironment(game_name, frames, sample_rate, channels)
    game.run_game(mode=game.play_with_keys)

def play_with_dumb_matcher(game_name):
    sample_rate = 44100
    frames = 2 * sample_rate
    channels = 1
    voice_recorder = BasicVoiceRecorder(game_name)
    voice_recorder.record_commands(frames, sample_rate, channels)
    transformer = FFTFeatureExtractor(
        commands=BasicVoiceRecorder.GamesToCommands[game_name],
        command_records_path=BasicVoiceRecorder.SavePath
    )
    transformer.extract_features()
    files = glob(FFTFeatureExtractor.SavePath + '*')
    matcher = DumbMatcher(frames, sample_rate, channels, files)

    game = GameEnvironment(game_name, frames, sample_rate, channels)
    game.run_game(game.play_with_voice, matcher=matcher)

def play_with_martins_matcher(game_name):
    sample_rate = 44100
    frames = 882
    channels = 1
    voice_recorder = BasicVoiceRecorder(game_name)
    voice_recorder.record_commands(sample_rate, sample_rate, channels)
    files = glob(BasicVoiceRecorder.SavePath + '*')
    matcher = MartinsMatcher(frames, sample_rate, channels, files)

    game = GameEnvironment(game_name, frames, sample_rate, channels)
    game.run_game(game.play_with_voice, matcher=matcher)

def play_with_daniel_matcher(game_name):
    sample_rate = 16000
    frames = 1 * sample_rate
    channels = 1
    voice_recorder = AdvancedVoiceRecorder(game_name)
    voice_recorder.record_commands(frames, sample_rate, channels)
    transformer = MFCCFeatureExtractor(
        commands=AdvancedVoiceRecorder.GamesToCommands[game_name],
        command_records_path=AdvancedVoiceRecorder.SavePath
    )
    transformer.extract_features()
    files = glob(MFCCFeatureExtractor.SavePath + '*')
    matcher = DanielMatcher(frames, sample_rate, channels, files)

    game = GameEnvironment(game_name, frames, sample_rate, channels)
    game.run_game(game.play_with_voice, matcher=matcher)
