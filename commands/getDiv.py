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
from database import Database
from psycopg2 import errors

class Div(BaseCommand):

    def __init__(self):
        # A quick description for the help message
        description = "Get a div based of any region by using your player page: (match.tf for AsiaFortress)"
        # A list of parameters that the command will take as input
        # Parameters will be separated by spaces and fed to the 'params'
        # If no params are expected, leave this list empty or set it to None
        # argument in the handle() method
        params = ["Player page"]
        self.db = Database()
        super().__init__(description, params)

    async def handle(self, params, msg, client):
        link = params[0]
        divs = self.get_region(link)
        roles = msg.guild.roles # Gets the guilds roles
        
        exist_and_same, no_users = self.check_user_exists(str(msg.author.id), link)
        if no_users or exist_and_same:
            steam = await self.get_user_steam(link)
            self.insert_user(str(msg.author.id), link, steam, False)
            banned = self.check_banned(link)
            
            divs = ['banned'] if banned else divs
            
            await self.give_role(msg, roles, divs)  # Give the user a new role and remove newb role
            await self.purge_and_post(msg)             # Purge the messages in the channel and post a new embed
        else:
            #TODO update this to go into an admin log
            print('user already exists as another account!')
            divs = ['banned']
        
        await self.give_role(msg, roles, divs)  # Give the user a new role and remove newb role
        await self.purge_and_post(msg)   

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
        elif 'casual' in link:
            return ['casual']
        else:
            return ['None']

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
        embed.add_field(name="Casual", value=";div casual", inline=False)
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

    # Give the user their role
    async def give_role(self, msg, roles, divs):
        newb_role = [x for x in roles if x.name.lower() == 'newb'][0] # Gets the newb role for removal later
        
        # Remove current divs from the region
        for x in msg.author.roles:
            if len(divs[0].split(' ')) > 1:
                if divs[0].split(' ')[0].lower() in x.name.lower():
                    await msg.author.remove_roles(x)
        
        success = False
        for div in divs:
            for role in roles:
                if role.name.lower().replace(' ', '') == div.lower().replace(' ', ''): # parse the roles to make it easily searchableç        
                    # Add a new role to the user and remove the newb role
                    await self.add_remove_roles(msg, role, newb_role)
                    await msg.channel.send('{} has been given the {} role.'.format(msg.author.mention, div))
                    print('role given')
                    success = True
                    break
                # If the div is ugc then send a specific message
        if not success:
            await msg.channel.send('This is not a valid role type, please try again')
            sleep(5)
                
    async def get_user_steam(self, link):
        if 'etf2l' in link:
            return Etf2l.get_steam(link)
        return 'None'
    
    def insert_user(self, meber_id, Etf2l_link, steam, verified):
        try:
            self.db.insert_into_users(meber_id, Etf2l_link, steam, verified)
        except errors.UniqueViolation:
            print('user already exists')
    
    #Needs more thought before implementation
    def check_user_exists(self, member_id, link):
        #Checks if the member registering is trhe
        return self.db.check_user_exists(member_id, link)

    
    def check_banned(self, etf2l_link):
        if 'etf2l' in etf2l_link:
            return Etf2l.get_banned(etf2l_link)
        return False
