import discord
from commands.base_command import BaseCommand
from colour import Color


class EditRoleColor(BaseCommand):

    def __init__(self):
        description = "Edits the color of a role - use either a colour name or Hex code"
        params = ["role name", "color"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        role = ' '.join(params[:-1])  # Joins all params except the final to get a role name
        colour = params[-1]  # gets the colour desired
        admin = message.author.guild_permissions.administrator

        try:
            # Coverts from Color colour to a discord colour
            c = Color(colour).rgb
            r, g, b = int(c[0] * 100), int(c[1] * 100), int(c[2] * 100)
            c = discord.Colour.from_rgb(r, g, b)

            if admin:
                # Edits the users role with the new colour
                await self.edit_role(message, role, c)
            else:
                await message.channel.send('Insufficient rank.')
        except Exception:
            await message.channel.send('Unknown colour.')

    # Edits the desired role with a desired colour
    async def edit_role(self, message, role_str, color):
        roles = await message.guild.fetch_roles()
        found = False
        i = 0

        # Tries to find the desired role and edit it
        while i < len(roles) - 1 and not found:
            if roles[i].name.lower() == role_str.lower():
                await roles[i].edit(colour=color)
                await message.channel.send('Role has been edited.')
                found = True
            i += 1

        if not found:
            await message.channel.send('Role not found.')
