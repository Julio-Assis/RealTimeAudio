from GameEnvironment.GameEnvironment import GameEnvironment
from GameEnvironment.VoiceRecorder import VoiceRecorder
from GameEnvironment.CommandMatcher import CommandMatcher
from GameEnvironment.CommandFFTTransformer import CommandFFTTransformer

from glob import glob
import sys

if __name__ == '__main__':
  
    #
    # python keyboard_agent.py SpaceInvadersNoFrameskip-v4
    #
    game_name = 'MsPacman-v0' if len(sys.argv) < 2 else sys.argv[1]
    voice_recorder = VoiceRecorder(game_name)
    voice_recorder.record_commands()
    transformer = CommandFFTTransformer(
        commands=VoiceRecorder.GamesToCommands[game_name],
        command_records_path=VoiceRecorder.SavePath
    )
    transformer.record_transforms()
    files = glob(CommandFFTTransformer.SavePath + '*')
    matcher = CommandMatcher(files)
    game = GameEnvironment(game_name)
    game.run_game(game.play_with_voice, matcher=matcher)