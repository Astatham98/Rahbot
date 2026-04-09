import discord
from commands.base_command import BaseCommand


def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple.
    
    Args:
        hex_color: Hex color string (e.g., 'FF0055' or '#FF0055')
        
    Returns:
        Tuple of (r, g, b) values (0-255)
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def name_to_rgb(color_name: str) -> tuple:
    """Convert common color names to RGB tuple.
    
    Args:
        color_name: Color name (e.g., 'red', 'blue', 'green')
        
    Returns:
        Tuple of (r, g, b) values (0-255) or None if not found
    """
    color_map = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'cyan': (0, 255, 255),
        'magenta': (255, 0, 255),
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'orange': (255, 165, 0),
        'purple': (128, 0, 128),
        'pink': (255, 192, 203),
        'brown': (165, 42, 42),
        'gray': (128, 128, 128),
        'grey': (128, 128, 128),
    }
    return color_map.get(color_name.lower())


class EditRoleColor(BaseCommand):
    def __init__(self):
        description = "Edits the color of a role - use either a colour name or Hex code"
        params = ["role name", "color"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        role = " ".join(
            params[:-1]
        )  # Joins all params except the final to get a role name
        colour = params[-1]  # gets the colour desired
        admin = message.author.guild_permissions.administrator

        try:
            # Try hex color first
            if colour.startswith('#'):
                r, g, b = hex_to_rgb(colour)
            elif colour.startswith('0x') or len(colour) == 6:
                try:
                    # Try parsing as hex
                    r, g, b = hex_to_rgb(colour)
                except ValueError:
                    # Try as color name
                    rgb = name_to_rgb(colour)
                    if rgb:
                        r, g, b = rgb
                    else:
                        raise ValueError("Unknown color")
            else:
                # Try as color name
                rgb = name_to_rgb(colour)
                if rgb:
                    r, g, b = rgb
                else:
                    raise ValueError("Unknown color")
            
            discord_color = discord.Colour.from_rgb(r, g, b)

            if admin:
                # Edits the users role with the new colour
                await self.edit_role(message, role, discord_color)
            else:
                await message.channel.send("Insufficient rank.")
        except ValueError:
            await message.channel.send("Unknown colour.")
        except Exception:
            await message.channel.send("Unknown colour.")

    # Edits the desired role with a desired colour
    async def edit_role(self, message, role_str, color):
        roles = await message.guild.fetch_roles()
        found = False
        i = 0

        # Tries to find the desired role and edit it
        while i < len(roles) - 1 and not found:
            if roles[i].name.lower() == role_str.lower():
                await roles[i].edit(colour=color)
                await message.channel.send("Role has been edited.")
                found = True
            i += 1

        if not found:
            await message.channel.send("Role not found.")
