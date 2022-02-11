from commands.base_command import BaseCommand
from utils import get_emoji
from random import randint
from divgetters.etf2l_player_id_get import Etf2l
from divgetters.ozf_player_id_get import Ozfortress
from divgetters.asia_player_id_get import AsiaFortress
from divgetters.sa_player_id_get import SA
from time import sleep
from divgetters.rgl_player_id_get import RGL
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
        roles = msg.guild.roles # Gets the guilds roles

        
        await self.give_role(msg, roles, divs)  # Give the user a new role and remove newb role
        await self.purge_and_post(msg)             # Purge the messages in the channel and post a new embed

    # finds the region and returns its div based on the link adress
    def get_region(self, link):
        if 'etf2l' in link:
            return Etf2l().get_div(link)
        elif 'rgl' in link:
            return RGL().get_div(link)
        elif 'match.tf' in link:
            return AsiaFortress().get_div(link)
        elif 'ozfortress' in link:
            return Ozfortress().get_div(link)
        elif 'ugc' in link:
            return ['ugc']
        elif 'fbtf' in link:
            return SA().get_div(link)

    # Sends a welcome message to the channel
    async def welcome_message_embed(self, message):
        embed = discord.Embed(title="Step up and get your div here!",
                              description="Type ;div {your region profile here}", color=0x00d9ff)
        embed.add_field(name="EU", value=";div https://etf2l.org/forum/user/109984/", inline=False)
        embed.add_field(name="NA", value=";div https://rgl.gg/Public/PlayerProfile.aspx?p=76561198136056704&r=40",
                        inline=False)
        embed.add_field(name="OzFort", value=";div https://ozfortress.com/users/2533", inline=False)
        embed.add_field(name="Asia", value=";div https://match.tf/users/5640", inline=False)
        embed.add_field(name="SA", value=";div https://fbtf.tf/users/788", inline=False)
        embed.set_footer(text="If you get the incorrect rank or the bot misses a rank, contact Rahmed.")
        await message.channel.send(embed=embed)

    # purges all messages in the channel and posts the welcome embed
    async def purge_and_post(self, msg):
        sleep(1)
        await msg.channel.purge()
        await self.welcome_message_embed(msg)

    # Removes the newb role and adds the new desired rolle
    async def add_remove_roles(self, msg, role, newb_role):
        await msg.author.add_roles(role)
        await msg.author.remove_roles(newb_role)

    # Sends the user a dm
    async def send_dm(self, member):
        channel = await member.create_dm()
        await channel.send("""Unfortunately RGL does not allow us to get specific divs at the moment.
To get your requested RGL div, please DM rahmed.
You've been given newcomer at the moment so you can explore the server while you wait.""")

    # Give the user their role
    async def give_role(self, msg, roles, divs):
        newb_role = [x for x in roles if x.name.lower() == 'newb'][0] # Gets the newb role for removal later
        [await msg.author.remove_roles(x) for x in msg.author.roles if divs[0].split(' ')[0].lower() in x.name.lower()]
        for div in divs:
            for role in roles:
                if role.name.lower().replace(' ', '') == div.lower().replace(' ', ''): # parse the roles to make it easily searchableç        
                    # Add a new role to the user and remove the newb role
                    await self.add_remove_roles(msg, role, newb_role)
                    await msg.channel.send('{} has been given the {} role.'.format(msg.author.mention, div))
                    print('role given')
                    break
                # If the div is ugc then send a specific message
                elif div == 'ugc':
                    await msg.channel.send('We currently do not accept UGC profiles, please try another profile type.')
                    break
