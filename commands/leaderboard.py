from commands.base_command import BaseCommand
from database import Database
import discord
import utils
import settings
import math


class Leaderboard(BaseCommand):
    def __init__(self):
        self.db = Database()
        description = "Returns a leaderboard."
        params = None
        super().__init__(description, params)
        self.page = 1

    async def handle(self, params, message, client):
            db = self.db
            id, name, played = db.get_players_and_games_played()

            if len(params) > 0:
                member_id = self.clean_id(params[0])
                player = client.get_user(int(member_id))
                embed = self.get_player_rank(player, id, played)
                await message.channel.send(embed=embed)
            else:
                embed = self.create_embed(name, played)
                msg = await message.channel.send(embed=embed)
                await self.add_reactions(msg)
                while True:
                    reaction, user = await client.wait_for('reaction_add', check=self.check)
                    correct_emoji = await self.remove_reaction(msg, user, reaction)
                    if correct_emoji:
                        await self.change_page(msg, reaction, name, played)

    def create_embed(self, name, played):
        embed = discord.Embed(title="Leaderboard*", color=0x7434eb)
        team1_text = '\n'.join(name[(self.page-1)*25:self.page*25])
        team2_text = '\n'.join([str(x) for x in played[(self.page-1)*25:self.page*25]])
        rank = '\n'.join([str(x+1 + (25*(self.page-1))) for x in range(25)])

        embed.add_field(name="Rank", value=rank, inline=True)
        embed.add_field(name="Player", value=team1_text, inline=True)
        embed.add_field(name="Games Played", value=team2_text, inline=True)

        return embed


    def get_player_rank(self, member, ids, played):
        try:
            rank = ids.index(str(member.id))
            games_played = played[rank]

            embed = discord.Embed(title="Leaderboard", color=0x7434eb)

            embed.add_field(name="Rank", value=rank+1, inline=True)
            embed.add_field(name="Player", value=member.name, inline=True)
            embed.add_field(name="Games Played", value=games_played, inline=True)

            return embed
        except ValueError:
            embed = discord.Embed(title="WARNING", color=0xfc0303)
            embed.add_field(name="User not recognized", value="This user is currently not in the database", inline=True)

            return embed

    def clean_id(self, id):
        id = id.replace('>', '')
        return id.split('!')[-1]

    def check(self, reaction, user):
        return not user.bot

    async def remove_reaction(self, msg, user, emoji):
        # Removes reactions from the message, if desired emoji return the true
        await msg.remove_reaction(emoji, user)

        if str(emoji) not in (str(utils.get_emoji("arrow_backward")), str(utils.get_emoji("arrow_forward"))):
            return False
        return True
    
    async def add_reactions(self, msg):
        await msg.add_reaction(utils.get_emoji("arrow_backward"))
        await msg.add_reaction(utils.get_emoji("arrow_forward"))

    async def change_page(self, msg, reaction, name, played):
        if str(reaction) == str(utils.get_emoji("arrow_forward")) and self.page + 1 <= math.ceil(len(name)/25):
            self.page += 1
        elif str(reaction) == str(utils.get_emoji("arrow_backward")) and self.page - 1 > 0:
            self.page -= 1
        await msg.edit(embed=self.create_embed(name, played))


