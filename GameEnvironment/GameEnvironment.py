#!/usr/bin/env python
from __future__ import print_function

import gym
import time
import numpy as np
import threading
import sounddevice as sd

class GameEnvironment:

    UP_ARROW = 65362
    RIGHT_ARROW = 65363
    LEFT_ARROW = 65361
    DOWN_ARROW = 65364

    def __init__(self, game_name, frames, sample_rate, channels):
        self.frames = frames
        self.sample_rate = sample_rate
        self.channels = channels
        self.human_agent_action = 0
        self.human_wants_restart = False
        self.human_sets_pause = False
        self.pause_key = 32
        self.restart_key = 0xff0d
        self.game_name = game_name
        self.env = []
        self.game_error = False
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

        print('ACTIONS={}'.format(self.ACTIONS))

        self.env.render()

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

    def play_with_keys(self):
        self.env.unwrapped.viewer.window.on_key_press = self.key_press
        self.env.unwrapped.viewer.window.on_key_release = self.key_release

    def play_random(self):
        while True:
            play = np.random.randint(1,5)
            self.human_agent_action = play
            time.sleep(0.5)

    def play_with_voice(self, matcher = None):

        play = True
        if matcher == None:
            self.game_error = 'To play with voice you have to provide a matcher'
            play = False

        while play:
            print('-'*20)
            print('recording new command...')
            command_signal = sd.rec(
                frames=self.frames,
                samplerate=self.sample_rate,
                channels=self.channels,
                blocking=True)
            action = matcher.get_closest(command_signal)
            print('your command: ' + action)
            self.set_agent_action(action)

    def set_agent_action(self, action):

        if action == 'LEFT':
            self.human_agent_action = 3
        elif action == 'UP':
            self.human_agent_action = 1
        elif action == 'RIGHT':
            self.human_agent_action = 2
        elif action == 'DOWN':
            self.human_agent_action = 4
        else:
            return

    def rollout(self):
        self.human_wants_restart = False
        obser = self.env.reset()
        skip = 0
        total_reward = 0
        total_timesteps = 0
        while 1 and not self.game_error:
            if not skip:
                a = self.human_agent_action
                total_timesteps += 1
                skip = self.SKIP_CONTROL
            else:
                skip -= 1

            obser, r, done, info = self.env.step(a)
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

    def run_game(self, mode, matcher=None):

        if matcher:
            t = threading.Thread(target=mode, args=(matcher,))
        else:
            t = threading.Thread(target=mode)
        t.start()

        while 1 and not self.game_error:
            window_still_open = self.rollout()
            if window_still_open == False:
                break

        if self.game_error:
            print(self.game_error)