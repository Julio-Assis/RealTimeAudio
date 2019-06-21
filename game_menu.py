from GameEnvironment.GameEnvironment import GameEnvironment
from GameEnvironment.DumbMatcher import DumbMatcher
import sys

def get_inputs_and_play(game_name, frames, sample_rate, channels, files):
    
    greeting_message()
    game_mode = get_game_mode()
    game_mode = validate_game_mode(game_mode)
    execute_game_mode(game_name, game_mode, frames, sample_rate, channels, files)

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

def execute_game_mode(game_name, game_mode, frames, sample_rate, channels, files):

    game = GameEnvironment(game_name, frames, sample_rate, channels)
        
    if game_mode == 1:
        game.run_game(mode=game.play_random)
    elif game_mode == 2:
        game.run_game(mode=game.play_with_keys)
    elif game_mode == 3:
        matcher = DumbMatcher(frames, sample_rate, channels, files)
        game.run_game(game.play_with_voice, matcher=matcher)
    elif game_mode == 4:
        raise Exception('Not implemented matcher.')
    elif game_mode == 5:
        raise Exception('Not implemented matcher.')
    else:
        print('Bye bye')
        sys.exit()

    
    