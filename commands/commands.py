from commands.base_command import BaseCommand
import settings
import discord


# This is a convenient command that automatically generates a helpful
# message showing all available commands
class Commands(BaseCommand):

    def __init__(self):
        description = "Displays this help message"
        params = None
        super().__init__(description, params)

    async def handle(self, params, message, client):
        from message_handler import COMMAND_HANDLERS
        msg = ""

        # Displays all descriptions, sorted alphabetically by command name
        for cmd in sorted(COMMAND_HANDLERS.items()):
            if not message.author.guild_permissions.administrator and cmd[0] not in settings.ADMIN_COMMANDS:
                msg += "\n" + cmd[1].description
            elif message.author.guild_permissions.administrator:
                msg += "\n" + cmd[1].description

        embed = discord.Embed(title="Commands", color=0xff0055)
        embed.add_field(name="User Commands", value=msg, inline=True)

        await message.channel.send(embed=embed)
