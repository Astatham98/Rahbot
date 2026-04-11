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
    admin_commands = {x.lower() for x in settings.ADMIN_COMMANDS}
    commands_attr = getattr(ctx.bot, "application_commands", None)
    if commands_attr is None:
        commands_attr = getattr(ctx.bot, "pending_application_commands", [])

    slash_commands = sorted(commands_attr, key=lambda x: x.name)

    # Displays all slash command descriptions, sorted alphabetically by command name
    for cmd in slash_commands:
        command_name = cmd.name.lower()
        cmd_perms = getattr(cmd, "default_member_permissions", None)
        is_admin_permission_command = False

        if cmd_perms is not None:
            try:
                is_admin_permission_command = bool(getattr(cmd_perms, "administrator", False))
            except Exception:
                is_admin_permission_command = False

            if not is_admin_permission_command:
                try:
                    admin_bit = discord.Permissions(administrator=True).value
                    is_admin_permission_command = bool(int(cmd_perms) & admin_bit)
                except Exception:
                    pass

        if (
            not ctx.author.guild_permissions.administrator
            and (command_name in admin_commands or is_admin_permission_command)
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