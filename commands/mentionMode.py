from commands.base_command import BaseCommand
import discord
import settings

class MentionMode(BaseCommand):
    def __init__(self):

        description = "Toggles the mention mode. 0 (default) for recommended teams, 1 for an embed of an ordered " \
                      "list of player names and divs. No parameters to see the current mode"
        params = None
        super().__init__(description, params)

    async def handle(self, params, message, client):
        admin = message.author.guild_permissions.administrator

        if not admin:
            await message.channel.send('Insufficient rank.')
        else:
            # if parameters are the desired length either find if its an incorrect input or
            # set the mention mode number in settings to the desired number
            if len(params) == 1:
                if int(params[0]) not in [0, 1]:
                    await message.channel.send('Incorrect input')
                else:
                    settings.MENTION_MODE = int(params[0])
                    await message.channel.send('Mention mode is now set to {}.'.format(settings.MENTION_MODE))
            elif len(params) == 0:
                # If no params are given return the current mention mode
                await message.channel.send('Mention mode is currently set to {}.'.format(settings.MENTION_MODE))
            else:
                await message.channel.send('Incorrect parameter input.')

