from GameEnvironment.GameEnvironment import GameEnvironment
from GameEnvironment.VoiceRecorder import VoiceRecorder
from GameEnvironment.DumbMatcher import DumbMatcher
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
    frames = 2 * 44100
    sample_rate = 44100
    channels = 1
    matcher = DumbMatcher(frames, sample_rate, channels, files)
    game = GameEnvironment(game_name, frames, sample_rate, channels)
    game.run_game(game.play_with_voice, matcher=matcher)
