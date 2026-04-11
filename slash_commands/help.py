import discord
import settings
from pagination import ButtonPaginationView, split_text_pages


def create_embed(msg, page_index=0, total_pages=1):
    embed = discord.Embed(title="Commands", color=0xFF0055)
    embed.add_field(name="User Commands", value=msg, inline=True)
    embed.set_footer(text=f"Page {page_index + 1}/{total_pages}")
    return embed


async def help_slash(ctx: discord.ApplicationContext):
    msg = ""
    commands_attr = getattr(ctx.bot, "application_commands", None)
    if commands_attr is None:
        commands_attr = getattr(ctx.bot, "pending_application_commands", [])

    slash_commands = sorted(commands_attr, key=lambda x: x.name)

    # Displays all slash command descriptions, sorted alphabetically by command name
    for cmd in slash_commands:
        if (
            not ctx.author.guild_permissions.administrator
            and cmd.name.lower() in settings.ADMIN_COMMANDS
        ):
            continue

        desc = cmd.description if cmd.description else "No description"
        msg += f"\n/{cmd.name} - {desc}"

    if msg.strip() == "":
        msg = "\nNo slash commands available."

    msg_pages = split_text_pages(msg)

    # Create pagination view with buttons
    view = ButtonPaginationView(msg_pages, create_embed, ctx.author.id)
    embed = view.current_embed()
    await ctx.respond(embed=embed, view=view)