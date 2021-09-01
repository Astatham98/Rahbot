from commands.base_command  import BaseCommand
from utils                  import get_emoji
from random                 import randint
from divgetters.etf2l_player_id_get import Etf2l
from divgetters.ozf_player_id_get import Ozfortress
from divgetters.asia_player_id_get import AsiaFortress

class Div(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Gets the div of the player based on their etf2l ID."
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # If no params are expected, leave this list empty or set it to None
        # argument in the handle() method
        params = ["ID"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        div = self.get_region(params[0])

        roles = message.guild.roles
        for role in roles:
            if div.lower() in role.name.lower():
                if div.lower() == 'rgl':
                    await message.channel.send('{} has been given the {} role. Tell Sigafoo to make a public API if you want divs.'.format(message.author.mention, div))
                else:
                    await message.author.add_roles(role)
                    await message.channel.send('{} has been given the {} role.'.format(message.author.mention, div))


    def get_region(self, link):
        if 'etf2l' in link:
            return Etf2l().get_div(link)
        elif 'rgl' in link:
            return 'RGL'
        elif 'match.tf' in link:
            return AsiaFortress().get_div(link)
        elif 'ozfortress' in link:
            return Ozfortress().get_div(link)
