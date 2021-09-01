import os
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

# The prefix that will be used to parse commands.
# It doesn't have to be a single character!
COMMAND_PREFIX = ";"


# The bot token. Keep this secret!
BOT_TOKEN = os.environ.get('RAHBOT_KE') if os.environ.get('RAHBOT_KEY') is not None else config.get('KEYS', 'key')

print(BOT_TOKEN)
# The now playing game. Set this to anything false-y ("", None) to disable it
NOW_PLAYING = COMMAND_PREFIX + "commands"

# Base directory. Feel free to use it if you want.
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
