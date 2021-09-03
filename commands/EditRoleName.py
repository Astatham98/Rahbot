import discord
from commands.base_command  import BaseCommand
from colour import Color
from div_colors import div_colours
import re

class EditRoleName(BaseCommand):
    def __init__(self):
        description = """Edits the name of a role - Use brackets for the name e.g. (ETF2L - PREMIERSHIP) (ETF2L - 6S PREMIERSHIP). 
type true to enable mass (will stitch new name to the end of the current roles)"""

        params = ["role name", "new name", 'mass']
        super().__init__(description, params)

    
    async def handle(self, params, message, client):
        parms = ' '.join(params)
        print(parms)
        names = parms.split(')')
        names = [x.replace('(', '') for x in names]
        print(names)
        role = names[0]
        new_name = names[1]
        
        mass = True if params[-1].lower().strip() == 'true' else False
        admin = message.author.guild_permissions.administrator
        print(role, new_name, len(params), mass)
        
        if len(names) > 2:
            await message.channel.send('Please input roles correctly')
        elif not admin:
            await message.channel.send('Insufficient rank')
        else:
            await self.edit_role(message, role, new_name, mass)


    async def edit_role(self, message, role_str, new_name, mass):
        roles = await message.guild.fetch_roles()
        if not mass:
            found=False
            i=0
            
            while i<len(roles)-1 and not found:
                if roles[i].name.lower() == role_str.lower():
                    await roles[i].edit(name=new_name)
                    await message.channel.send('Role has been edited.')
                    found=True
                i+=1
                    
            if not found:
                await message.channel.send('Role not found.')
        else:
            await self.mass_edit_roles(message, roles, new_name)
        
    async def mass_edit_roles(self, message, roles, new_name):
        div_names = [x.lower() for x in div_colours.keys()]
        discord_roles = [x for x in roles if x.name.lower() in div_names and x.name.lower != 'newb']
        for role in discord_roles:
            await role.edit(name=role.name + ' ' + new_name)
        
        await message.channel.send('Roles successfully mass updated')
        