import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# The prefix that will be used to parse commands.
# It doesn't have to be a single character!
COMMAND_PREFIX = ";"

# The bot token. Keep this secret!
BOT_TOKEN = os.environ.get('RAHBOT_KEY') if os.environ.get('RAHBOT_KEY') is not None else config.get('KEYS', 'RAHBOT_KEY')


print(BOT_TOKEN)
# The now playing game. Set this to anything false-y ("", None) to disable it
NOW_PLAYING = COMMAND_PREFIX + "commands"

# Base directory. Feel free to use it if you want.
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

CHANNEL = ["get-yo-div-here", "mod-bot-stuff", "b0t-trash", "eu-servers", "na-servers"]
TRACK = "pug"

# mention mode toggle
MENTION_MODE = 1

# The id of the last played match
LAST_PLAYED = []

CURRENT_GAME = {}

ADMIN_COMMANDS = ['editrolecolor', 'editrolename', 'mentionmode', 'rundb', 'setup', 'setupdb']

