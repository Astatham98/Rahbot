import discord
from discord import slash_command
from discord.ui import Button, View
import settings
from message_handler import COMMAND_HANDLERS


class HelpPaginationView(View):
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


def parsetext(text):
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


def create_embed(msg):
    embed = discord.Embed(title="Commands", color=0xFF0055)
    embed.add_field(name="User Commands", value=msg, inline=True)
    return embed


@slash_command(name="help", description="Displays help message with all available commands")
async def help_slash(ctx: discord.ApplicationContext):
    msg = ""

    # Displays all descriptions, sorted alphabetically by command name
    for cmd in sorted(COMMAND_HANDLERS.items()):
        if (
            not ctx.author.guild_permissions.administrator
            and cmd[0] not in settings.ADMIN_COMMANDS
        ):
            msg += "\n" + cmd[1].description
        elif ctx.author.guild_permissions.administrator:
            msg += "\n" + cmd[1].description

    msg_pages = parsetext(msg)

    # Create pagination view with buttons
    view = HelpPaginationView(msg_pages, create_embed)
    embed = create_embed(msg_pages[0])
    await ctx.respond(embed=embed, view=view)