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
        div = self.get_region(params[0])

        roles = msg.guild.roles
        for role in roles:
            if role.name.lower() in div.lower():
                if div.lower() == 'rgl':
                    await msg.author.add_roles(role)
                    await msg.channel.send('{} has been given the {} role. Tell Sigafoo to make a public API if you want divs.'.format(message.author.mention, div))
                    await self.purge_and_post(msg)
                    break
                else:
                    await msg.author.add_roles(role)
                    await msg.channel.send('{} has been given the {} role.'.format(msg.author.mention, div))
                    await self.purge_and_post(msg)
                    break


    def get_region(self, link):
        if 'etf2l' in link:
            return Etf2l().get_div(link)
        elif 'rgl' in link:
            return 'RGL'
        elif 'match.tf' in link:
            return AsiaFortress().get_div(link)
        elif 'ozfortress' in link:
            return Ozfortress().get_div(link)
        
    async def welcome_message_embed(self, message):
        embed=discord.Embed(title="Step up and get your role!", description="Get your own role based on your division in any region!", color=0xe69100)
        embed.add_field(name="Simply type ;div {region link here}", value="Use; etf2l for EU, RGL for NA, match.tf for Asia Pacific, and OzFortress for AU.", inline=True)
        embed.set_footer(text="Enjoy your say :).")
        await message.channel.send(embed=embed)
        
    async def purge_and_post(self, msg):
        sleep(1)
        await msg.channel.purge()
        await self.welcome_message_embed(msg)