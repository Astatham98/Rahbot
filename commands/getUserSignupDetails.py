from commands.base_command import BaseCommand
from database import Database
import utils
import re
import discord


class GetUserAccounts(BaseCommand):
    def __init__(self):
        description = "Gets the users account"

        params = ["@user, etf2l, steam64"]
        super().__init__(description, params)
        self.db = Database()
        
    async def handle(self, params, message, client):
        user_details = await self.get_user_accounts(params, message)
        discord_user = client.get_user(int(user_details[0]))
        embed = self.generate_embed(discord_user, user_details)
        await message.channel.send(embed=embed)
        

    async def get_user_accounts(self, params, message):
        query_type = None
        query = params[0]
        if '@' in query:
            query = utils.parse_mention(query)
            query_type = 'id'
        elif 'etf2l' in query:
            query_type = 'linkedProfile'
        else:
            replaced_query = query.replace("https://steamcommunity.com", "")
            pattern = """(?P<CUSTOMPROFILE>https?\:\/\/steamcommunity\.com\/id\/
            [A-Za-z_0-9]+)|(?P<CUSTOMURL>\/id\/[A-Za-z_0-9]+)|(?P<PROFILE>https?
            \:\/\/steamcommunity.com\/profiles\/[0-9]+)|(?P<STEAMID2>STEAM_[10]:
            [10]:[0-9]+)|(?P<STEAMID3>\[U:[10]:[0-9]+\])|(?P<STEAMID64>[^\/][0-9]{8,})"""
            is_steam = re.match(pattern, replaced_query)
            if is_steam:
                #TODO convert to other values
                query_type = 'steam'
                
        if query_type is not None:
            return self.db.get_user_accounts(query_type, query)
        else:
            await message.channel.send_message("Invalid user")
            return
        
    def generate_embed(self, discord_user, user_details):
        username = discord_user.display_name
        linked_profile = user_details[1]
        steam = user_details[2]
        registered_date = user_details[3]
        verified = user_details[4]
        embed = discord.Embed(title=username, colour=discord.Colour.blue())
        
        text = f"Profile: {linked_profile}\nSteam: {steam}\nDate Registered: {registered_date}\nVerified: {verified}"
        embed.add_field(name="Details", value=text, inline=True)
        return embed
        