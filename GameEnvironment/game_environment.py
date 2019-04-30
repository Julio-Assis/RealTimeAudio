#!/usr/bin/env python
from __future__ import print_function

import sys, gym, time

#
# Run the game with different environments! Pass environment name as a command-line argument, for example:
#
# python game_environment.py SpaceInvadersNoFrameskip-v4
#

env = gym.make('MsPacman-v0' if len(sys.argv)<2 else sys.argv[1])

if not hasattr(env.action_space, 'n'):
    raise Exception('Keyboard agent only supports discrete action spaces')
ACTIONS = env.action_space.n
SKIP_CONTROL = 0    # Use previous control decision SKIP_CONTROL times, that's how you
                    # can test what skip is still usable.

human_agent_action = 0
human_wants_restart = False
human_sets_pause = False

def key_press(key, mod):
    print("Displaying key here")
    print(key)
    global human_agent_action, human_wants_restart, human_sets_pause
    if key == 65361:
        human_agent_action = 3
    elif key == 65362:
        human_agent_action = 1
    elif key == 65363:
        human_agent_action = 2
    elif key == 65364:
        human_agent_action = 4
    else:
        return

def key_release(key, mod):
    global human_agent_action
    a = int( key - ord('0') )
    if a <= 0 or a >= ACTIONS: return
    if human_agent_action == a:
        human_agent_action = 0

env.render()
env.unwrapped.viewer.window.on_key_press = key_press
env.unwrapped.viewer.window.on_key_release = key_release

def rollout(env):
    global human_agent_action, human_wants_restart, human_sets_pause
    human_wants_restart = False
    obser = env.reset()
    skip = 0
    total_reward = 0
    total_timesteps = 0
    while 1:
        if not skip:
            a = human_agent_action
            total_timesteps += 1
            skip = SKIP_CONTROL
        else:
            skip -= 1

        obser, r, done, info = env.step(a)

        total_reward += r
        window_still_open = env.render()
        if window_still_open==False: return False
        if done: break
        if human_wants_restart: break
        while human_sets_pause:
            env.render()
            time.sleep(0.1)
        time.sleep(0.1)

print("ACTIONS={}".format(ACTIONS))

while 1:
    window_still_open = rollout(env)
    if window_still_open==False: break

# commands = {
#     1: "UP", 65362
#
#     2: "RIGHT", 65363
#
#     3: "LEFT", 65361
#
#     4 : "DOWN", 65364
#
# }
