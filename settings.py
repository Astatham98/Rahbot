import os

# The prefix that will be used to parse commands.
# It doesn't have to be a single character!
COMMAND_PREFIX = ";"

# The bot token. Keep this secret!
BOT_TOKEN = "NjkxMjE4NzUzNDc5OTAxMjE1.XncxoQ.PfwwoolIX4iA4o7a1HjYOFamhWI"

# The now playing game. Set this to anything false-y ("", None) to disable it
NOW_PLAYING = COMMAND_PREFIX + "commands"

# Base directory. Feel free to use it if you want.
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
