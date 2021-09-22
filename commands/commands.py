import discord
import utils
import settings
from commands.base_command import BaseCommand


# This is a convenient command that automatically generates a helpful
# message showing all available commands
class Commands(BaseCommand):

    def __init__(self):
        description = "Displays this help message"
        params = None
        super().__init__(description, params)
        self.page = 1

    async def handle(self, params, message, client):
        from message_handler import COMMAND_HANDLERS
        msg = ""

        # Displays all descriptions, sorted alphabetically by command name
        for cmd in sorted(COMMAND_HANDLERS.items()):
            if not message.author.guild_permissions.administrator and cmd[0] not in settings.ADMIN_COMMANDS:
                msg += "\n" + cmd[1].description
            elif message.author.guild_permissions.administrator:
                msg += "\n" + cmd[1].description

        msg_pages = self.parsetext(msg)

        embed = self.create_embed(msg_pages[0])
        msg = await message.channel.send(embed=embed)
        await self.add_reactions(msg)
        while True:
            reaction, user = await client.wait_for('reaction_add', check=self.check)
            correct_emoji = await self.remove_reaction(msg, user, reaction)
            if correct_emoji:
                await self.change_page(msg_pages, msg, reaction, len(msg_pages))

    def parsetext(self, text):
        """Parses text into seperate strings to """
        splittext = text.split('\n')

        page_content = []
        lines = ""
        for line in splittext:
            if len(lines) + len(line) > 1000:
                page_content.append(lines)
                lines = line
            else:
                lines += line + '\n'
        page_content.append(lines)

        return page_content

    def check(self, reaction, user):
        return not user.bot

    async def remove_reaction(self, msg, user, emoji):
        # Removes reactions from the message, if desired emoji return the true
        await msg.remove_reaction(emoji, user)

        if str(emoji) not in (str(utils.get_emoji("arrow_backward")), str(utils.get_emoji("arrow_forward"))):
            return False
        return True

    async def add_reactions(self, msg):
        await msg.add_reaction(utils.get_emoji("arrow_backward"))
        await msg.add_reaction(utils.get_emoji("arrow_forward"))

    async def change_page(self, msgs, msg, reaction, pages):
        if str(reaction) == str(utils.get_emoji("arrow_forward")) and self.page + 1 <= pages:
            self.page += 1
        elif str(reaction) == str(utils.get_emoji("arrow_backward")) and self.page - 1 > 0:
            self.page -= 1
        await msg.edit(embed=self.create_embed(msgs[self.page-1]))

    def create_embed(self, msg):
        embed = discord.Embed(title="Commands", color=0xff0055)
        embed.add_field(name="User Commands", value=msg, inline=True)
        return embed
