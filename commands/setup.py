from commands.base_command  import BaseCommand
from div_colors import div_colours
import discord

class setup(BaseCommand):

    def __init__(self):
       
        description = "Setup roles for a new server"
        params = None
        super().__init__(description, params)

    async def handle(self, params, message, client):
        roles = await message.guild.fetch_roles()
        role_names = [x.name for x in roles]
        admin = message.author.guild_permissions.administrator
        
        for gamemode in ["6's", "highlander"]:
            if 'ETF2L - Premiership' + ' ' + gamemode not in role_names and admin:
                #Excludes rgl and newb role from getting a gamemode tag
                for name, col in list(div_colours.items())[:-2]:
                    print(name, col)
                    await self.create_role(message, name + ' ' + gamemode, col)
                
                #If RGL or newb role don't exist, add them 
                for name, col in list(div_colours.items())[:-2]:
                    if name not in role_names:
                        await self.create_role(message, name, col)
                await message.channel.send(gamemode + ' Roles have been added')
                print('Roles added')
            elif not admin:
                print('Not admin')
                await message.channel.send('You do not have permission to run this command')
            else:
                #await self.edit_roles_color(message)
                print('Has roles')
                await message.channel.send('This server already has the required roles for ' + gamemode)

    
    async def create_role(self, message, dregion, color):
        guild = message.guild
        await guild.create_role(name=dregion, color=color)
    
    
    async def edit_roles_color(self, message):
        roles = await message.guild.fetch_roles()
        for role in roles:
            try:
                color = div_colours.get(role.name, role.colour)
                await role.edit(colour=color)
            except discord.errors.Forbidden:
                pass
    