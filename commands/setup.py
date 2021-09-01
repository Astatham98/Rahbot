from commands.base_command  import BaseCommand
import div_colors as col


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
            
            #AsiaFortress
            await self.create_role(message, 'AsiaFortress - Division 1', col.PREM)
            await self.create_role(message, 'AsiaFortress - Division 2', col.DIV2)
            await self.create_role(message, 'AsiaFortress - Division 3', col.MID)
            await self.create_role(message, 'AsiaFortress - Division 4', col.OPEN)

            #ETF2L
            await self.create_role(message, 'ETF2L - Premiership', col.PREM)
            await self.create_role(message, 'ETF2L - Division 1', col.DIV1)
            await self.create_role(message, 'ETF2L - Division 2', col.DIV2)
            await self.create_role(message, 'ETF2L - Mid', col.MID)
            await self.create_role(message, 'ETF2L - Low', col.LOW)
            await self.create_role(message, 'ETF2L - Open', col.OPEN)

            #Ozfortress
            await self.create_role(message, 'OzFortress - Premier', col.PREM)
            await self.create_role(message, 'OzFortress - Intermediate', col.DIV2)
            await self.create_role(message, 'OzFortress - Main', col.MID)
            await self.create_role(message, 'OzFortress - Open', col.OPEN)

            #RGL
            await self.create_role(message, 'RGL', col.RGL)

            await message.channel.send('Roles have been added')
            print('Roles added')
        elif not admin:
            print('Not admin')
            await message.channel.send('You do not have permission to run this command')
        else:
            print('Has roles')
            await message.channel.send('This server already has the required roles')

    async def create_role(self, message, dregion, color):
        guild = message.guild
        await guild.create_role(name=dregion, color=color)