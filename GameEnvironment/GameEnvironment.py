################### ORIGINAL ########################
#!/usr/bin/env python
from __future__ import print_function

import sys
import gym
import time


class GameEnvironment:

    UP_ARROW = 65362
    RIGHT_ARROW = 65363
    LEFT_ARROW = 65361
    DOWN_ARROW = 65364

    def __init__(self, game_name):
        self.human_agent_action = 0
        self.human_wants_restart = False
        self.human_sets_pause = False
        self.pause_key = 32
        self.restart_key = 0xff0d
        self.game_name = game_name
        self.env = []
        self.create_env()

    def create_env(self):

        self.env = gym.make(self.game_name)
        if not hasattr(self.env.action_space, 'n'):
            raise Exception(
                'Keyboard agent only supports discrete action spaces')
        self.ACTIONS = self.env.action_space.n
        # Use previous control decision SKIP_CONTROL times, that's how you
        self.SKIP_CONTROL = 0
        # can test what skip is still usable.

        print("ACTIONS={}".format(self.ACTIONS))

        self.env.render()
        self.env.unwrapped.viewer.window.on_key_press = self.key_press
        self.env.unwrapped.viewer.window.on_key_release = self.key_release

    def key_press(self, key, mod):

        if key == self.restart_key:
            self.human_wants_restart = True

        if key == self.pause_key:
            self.human_sets_pause = not self.human_sets_pause

        a = int(key - ord('0'))
        if a <= 0 or a >= self.ACTIONS:
            return

        self.human_agent_action = a

    def key_release(self, key, mod):

        if key == GameEnvironment.LEFT_ARROW:
            self.human_agent_action = 3
        elif key == GameEnvironment.UP_ARROW:
            self.human_agent_action = 1
        elif key == GameEnvironment.RIGHT_ARROW:
            self.human_agent_action = 2
        elif key == GameEnvironment.DOWN_ARROW:
            self.human_agent_action = 4
        else:
            return

    def rollout(self):
        self.human_wants_restart = False
        obser = self.env.reset()
        skip = 0
        total_reward = 0
        total_timesteps = 0
        while 1:
            if not skip:
                a = self.human_agent_action
                total_timesteps += 1
                skip = self.SKIP_CONTROL
            else:
                skip -= 1

            obser, r, done, info = self.env.step(a)
            if r != 0:
                print("reward %0.3f" % r)
            total_reward += r
            window_still_open = self.env.render()
            if window_still_open == False:
                return False
            if done:
                break
            if self.human_wants_restart:
                break
            while self.human_sets_pause:
                self.env.render()
                time.sleep(0.1)
            time.sleep(0.1)
        print("timesteps %i reward %0.2f" % (total_timesteps, total_reward))

    def run_game(self):
        
        while 1:
            window_still_open = self.rollout()
            if window_still_open == False:
                break


if __name__ == "__main__":

    #
    # Test yourself as a learning agent! Pass environment name as a command-line argument, for example:
    #
    # python keyboard_agent.py SpaceInvadersNoFrameskip-v4
    #
    game_name = 'MsPacman-v0' if len(sys.argv) < 2 else sys.argv[1]
    game = GameEnvironment(game_name)
    game.run_game()