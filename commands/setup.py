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
        if 'ETF2L - Premiership' not in role_names and admin:
            for name, col in div_colours.items():
                print(name, col)
                await self.create_role(message, name, col)
            
            await message.channel.send('Roles have been added')
            print('Roles added')
        elif not admin:
            print('Not admin')
            await message.channel.send('You do not have permission to run this command')
        else:
            await self.edit_roles(message)
            print('Has roles')
            await message.channel.send('This server already has the required roles')

    
    async def create_role(self, message, dregion, color):
        guild = message.guild
        await guild.create_role(name=dregion, color=color)
    
    
    async def edit_roles(self, message):
        roles = await message.guild.fetch_roles()
        for role in roles:
            try:
                color = div_colours.get(role.name, role.colour)
                await role.edit(colour=color)
            except discord.errors.Forbidden:
                pass
            