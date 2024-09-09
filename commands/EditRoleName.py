from commands.base_command import BaseCommand
from div_colors import div_colours


class EditRoleName(BaseCommand):
    def __init__(self):
        description = """Edits the name of a role - Use brackets for the name e.g. (ETF2L - PREMIERSHIP) (ETF2L - 6S PREMIERSHIP). 
true to enable or disable mass editing"""

        params = ["role name", "new name", "mass"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        parms = " ".join(params)  # Joins all the params together
        names = parms.split(")")  # Splits params and replace the opening bracket
        names = [x.replace("(", "") for x in names]
        role = names[0]
        new_name = names[1]

        # check if the user wants to mass change ranks
        mass = True if params[-1].lower().strip() == "true" else False
        admin = message.author.guild_permissions.administrator
        print(role, new_name, len(names), mass)

        if len(names) > 3:
            await message.channel.send("Please input the command correctly")
        elif not admin:
            await message.channel.send("Insufficient rank.")
        else:
            await self.edit_role(message, role, new_name, mass)

    # Edits the role based on the old and the new name
    async def edit_role(self, message, role_str, new_name, mass):
        roles = await message.guild.fetch_roles()
        if not mass:  # If its not a mass edit
            found = False
            i = 0
            # Search for the role and edit its name
            while i < len(roles) - 1 and not found:
                if roles[i].name.lower() == role_str.lower():
                    await roles[i].edit(name=new_name)
                    await message.channel.send("Role has been edited.")
                    found = True
                i += 1

            if not found:
                await message.channel.send("Role not found.")
        else:
            # mass edit
            await self.mass_edit_roles(message, roles, new_name)

    # Mass edits all the names in the div_colours with the new desired ender
    async def mass_edit_roles(self, message, roles, new_name):
        div_names = [x.lower() for x in div_colours.keys()]
        # Gets the names that are the same in the current discord that are in the div_names
        discord_roles = [
            x for x in roles if x.name.lower() in div_names and x.name.lower != "newb"
        ]
        for role in discord_roles:
            await role.edit(
                name=role.name + " " + new_name
            )  # Edits the names with the new ender

        await message.channel.send("Roles successfully mass updated")
