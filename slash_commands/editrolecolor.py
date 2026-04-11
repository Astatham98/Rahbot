"""Edit role color slash command."""

import discord


def hex_to_rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def name_to_rgb(color_name: str):
    color_map = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "orange": (255, 165, 0),
        "purple": (128, 0, 128),
        "pink": (255, 192, 203),
        "brown": (165, 42, 42),
        "gray": (128, 128, 128),
        "grey": (128, 128, 128),
    }
    return color_map.get(color_name.lower())


async def editrolecolor_slash(
    ctx: discord.ApplicationContext,
    role_name: str,
    color: str,
):
    """Edit a role color with color name or hex value (admin only)."""
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond("Insufficient rank.", ephemeral=True)
        return

    try:
        if color.startswith("#"):
            r, g, b = hex_to_rgb(color)
        elif color.startswith("0x") or len(color) == 6:
            try:
                r, g, b = hex_to_rgb(color)
            except ValueError:
                rgb = name_to_rgb(color)
                if not rgb:
                    raise ValueError("Unknown color")
                r, g, b = rgb
        else:
            rgb = name_to_rgb(color)
            if not rgb:
                raise ValueError("Unknown color")
            r, g, b = rgb

        discord_color = discord.Colour.from_rgb(r, g, b)
    except Exception:
        await ctx.respond("Unknown colour.")
        return

    roles = await ctx.guild.fetch_roles()
    role = discord.utils.find(lambda x: x.name.lower() == role_name.lower(), roles)
    if role is None:
        await ctx.respond("Role not found.")
        return

    await role.edit(colour=discord_color)
    await ctx.respond("Role has been edited.")
