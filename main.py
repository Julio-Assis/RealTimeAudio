from game_menu import get_inputs_and_play
import sys

if __name__ == '__main__':

    #
    # python keyboard_agent.py SpaceInvadersNoFrameskip-v4
    #
    game_name = 'MsPacman-v0' if len(sys.argv) < 2 else sys.argv[1]
    get_inputs_and_play(game_name)
