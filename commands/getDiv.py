from commands.base_command  import BaseCommand
from utils                  import get_emoji
from random                 import randint
from divgetters.etf2l_player_id_get import Etf2l
from divgetters.ozf_player_id_get import Ozfortress
from divgetters.asia_player_id_get import AsiaFortress
from time import sleep
import discord

class Div(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Get a div based of any region by using your player page: (match.tf for AsiaFortress)"
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # If no params are expected, leave this list empty or set it to None
        # argument in the handle() method
        params = ["Player page"]
        super().__init__(description, params)

    async def handle(self, params, msg, client):
        divs = self.get_region(params[0])
        roles = msg.guild.roles
        
        for div in divs:
            await self.give_role(msg, roles, div)
        await self.purge_and_post(msg)

        

    def get_region(self, link):
        if 'etf2l' in link:
            return Etf2l().get_div(link)
        elif 'rgl' in link:
            return ['RGL - Newcomer']
        elif 'match.tf' in link:
            return AsiaFortress().get_div(link)
        elif 'ozfortress' in link:
            return Ozfortress().get_div(link)
        
    async def welcome_message_embed(self, message):
        embed=discord.Embed(title="Step up and get your div here!", description="Type ;div {your region profile here}", color=0x00d9ff)
        embed.add_field(name="EU", value=";div https://etf2l.org/forum/user/109984/", inline=False)
        embed.add_field(name="NA", value=";div https://rgl.gg/Public/PlayerProfile.aspx?p=76561198136056704&r=40", inline=False)
        embed.add_field(name="OzFort", value=";div https://ozfortress.com/users/2533", inline=False)
        embed.add_field(name="Asia", value=";div https://match.tf/users/5640", inline=False)
        await message.channel.send(embed=embed)
        
    async def purge_and_post(self, msg):
        sleep(1)
        await msg.channel.purge()
        await self.welcome_message_embed(msg)
        
    async def add_remove_roles(self, msg, role, newb_role):
        await msg.author.add_roles(role)
        await msg.author.remove_roles(newb_role)
    
    async def send_dm(self, member):
        channel = await member.create_dm()
        await channel.send("""Unfortunately RGL does not allow us to get specific divs at the moment.
To get your requested RGL div, please DM rahmed.
You've been given newcomer at the moment so you can explore the server while you wait.""")
        
    async def give_role(self, msg, roles, div):
        newb_role = [x for x in roles if x.name.lower() == 'newb'][0]
        for role in roles:
            if role.name.lower().replace(' ', '') == div.lower().replace(' ', ''):                
                if "rgl" in div.lower():
                    
                    await self.send_dm(msg.author)
                    print('rgl here 2')
                    await self.add_remove_roles(msg, role, newb_role)
                    print('rgl here 3')
                    await msg.channel.send('{} has been given the {} role. Tell Sigafoo to make a public API if you want divs.'.format(msg.author.mention, div))
                    break
                else:
                    await self.add_remove_roles(msg, role, newb_role)
                    await msg.channel.send('{} has been given the {} role.'.format(msg.author.mention, div))
                    print('role given')
                    break