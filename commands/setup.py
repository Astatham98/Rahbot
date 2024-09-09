from commands.base_command import BaseCommand
from div_colors import div_colours
import discord


class setup(BaseCommand):
    def __init__(self):
        description = "Setup roles for a new server"
        params = None
        super().__init__(description, params)

    # This code sucks and should be redone
    async def handle(self, params, message, client):
        roles = await message.guild.fetch_roles()  # Fetches the roles and role names
        role_names = [x.name for x in roles]
        admin = message.author.guild_permissions.administrator

        if len(params) > 0 and params[0] == "update":
            await self.update_roles(role_names, message)
            await message.channel.send("Updated roles")
            return

        # Goes through both gamemodes
        for gamemode in ["6's", "highlander"]:
            if "ETF2L - Premiership" + " " + gamemode not in role_names and admin:
                # Excludes rgl and newb role from getting a gamemode tag
                for name, col in list(div_colours.items())[:-2]:
                    print(name, col)
                    await self.create_role(message, name + " " + gamemode, col)

                # If RGL or newb role don't exist, add them
                for name, col in list(div_colours.items())[:-2]:
                    if name not in role_names:
                        await self.create_role(message, name, col)
                await message.channel.send(gamemode + " Roles have been added")
                print("Roles added")
            elif not admin:
                print("Not admin")
                await message.channel.send("Insufficient rank.")
            else:
                # await self.edit_roles_color(message)
                print("Has roles")
                await message.channel.send(
                    "This server already has the required roles for " + gamemode
                )

    # Creates a new role based on a string name and a colour
    async def create_role(self, message, dregion, color):
        guild = message.guild
        await guild.create_role(name=dregion, color=color)

    # Edits a specific roles' colour
    async def edit_roles_color(self, message):
        roles = await message.guild.fetch_roles()
        for role in roles:
            for gamemode in [" 6's", " highlander"]:
                try:
                    role_col_name = role.name.replace(gamemode, "")
                    if (
                        not discord.Color(
                            div_colours.get(role_col_name, role.colour.value)
                        )
                        == role.colour
                    ):
                        color = div_colours.get(role_col_name, role.colour)
                        await role.edit(colour=color)
                except discord.errors.Forbidden:
                    pass

    async def update_roles(self, serverRoles, msg):
        region_names = list(div_colours.keys())
        role_str = " ".join([x.lower() for x in serverRoles])
        new = []
        for name in region_names:
            if name.lower() not in role_str:
                new.append(name)

        for gamemode in [" 6's", " highlander"]:
            if len(new) > 0:
                [
                    await self.create_role(msg, x + gamemode, div_colours.get(x))
                    for x in new
                ]
            else:
                await self.edit_roles_color(msg)
