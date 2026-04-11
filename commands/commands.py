import discord
import settings
from commands.base_command import BaseCommand
from pagination import ButtonPaginationView, split_text_pages


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
            if (
                not message.author.guild_permissions.administrator
                and cmd[0] not in settings.ADMIN_COMMANDS
            ):
                msg += "\n" + cmd[1].description
            elif message.author.guild_permissions.administrator:
                msg += "\n" + cmd[1].description

        msg_pages = split_text_pages(msg)

        # Create pagination view with buttons
        view = ButtonPaginationView(msg_pages, self.create_embed, message.author.id)
        embed = view.current_embed()
        sent_msg = await message.channel.send(embed=embed, view=view)
        view.message = sent_msg

    def create_embed(self, msg, page_index=0, total_pages=1):
        embed = discord.Embed(title="Commands", color=0xFF0055)
        embed.add_field(name="User Commands", value=msg, inline=True)
        embed.set_footer(text=f"Page {page_index + 1}/{total_pages}")
        return embed
