import discord
from discord.ui import Button, View
import settings
from commands.base_command import BaseCommand


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

        msg_pages = self.parsetext(msg)

        # Create pagination view with buttons
        view = PaginationView(msg_pages, self.create_embed)
        embed = self.create_embed(msg_pages[0])
        await message.channel.send(embed=embed, view=view)

    def parsetext(self, text):
        """Parses text into seperate strings to"""
        splittext = text.split("\n")

        page_content = []
        lines = ""
        for line in splittext:
            if len(lines) + len(line) > 1000:
                page_content.append(lines)
                lines = line
            else:
                lines += line + "\n"
        page_content.append(lines)

        return page_content

    def create_embed(self, msg):
        embed = discord.Embed(title="Commands", color=0xFF0055)
        embed.add_field(name="User Commands", value=msg, inline=True)
        return embed


class PaginationView(View):
    def __init__(self, pages, create_embed_func):
        super().__init__(timeout=None)
        self.pages = pages
        self.current_page = 0
        self.create_embed = create_embed_func
        self._update_buttons()

    def _update_buttons(self):
        # Disable buttons when at first/last page
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page == len(self.pages) - 1

    @discord.ui.button(label="◀ Previous", style=discord.ButtonStyle.primary)
    async def prev_button(self, button: Button, interaction: discord.Interaction):
        if self.current_page > 0:
            self.current_page -= 1
            self._update_buttons()
            await interaction.response.edit_message(
                embed=self.create_embed(self.pages[self.current_page]),
                view=self
            )

    @discord.ui.button(label="Next ▶", style=discord.ButtonStyle.primary)
    async def next_button(self, button: Button, interaction: discord.Interaction):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self._update_buttons()
            await interaction.response.edit_message(
                embed=self.create_embed(self.pages[self.current_page]),
                view=self
            )
