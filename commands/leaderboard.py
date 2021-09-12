from commands.base_command import BaseCommand
from database import Database
import discord
import settings


class Leaderboard(BaseCommand):
    def __init__(self):
        self.db = Database()
        description = "Returns a leaderboard. If a player is mentioned after the command their rank will get displayed."
        params = None
        super().__init__(description, params)

    async def handle(self, params, message, client):
        if message.author.guild_permissions.administrator:
            db = self.db
            id, name, played = db.get_players_and_games_played()

            if len(params) > 0:
                member_id = self.clean_id(params[0])
                player = client.get_user(int(member_id))
                embed = self.get_player_rank(player, id, played)
                await message.channel.send(embed=embed)

            else:
                embed = self.create_embed(name, played)
                await message.channel.send(embed=embed)
        else:
            await message.channel.send('Insufficient rank.')

    def create_embed(self, name, played):
        embed = discord.Embed(title="!Divs", color=0x7434eb)
        team1_text = '\n'.join(name)
        team2_text = '\n'.join([str(x) for x in played])
        rank = '\n'.join([str(x+1) for x in range((len(name)))])

        embed.add_field(name="Rank", value=rank, inline=True)
        embed.add_field(name="Player", value=team1_text, inline=True)
        embed.add_field(name="Games Played", value=team2_text, inline=True)

        return embed

    def get_player_rank(self, member, ids, played):
        rank = ids.index(str(member.id))
        games_played = played[rank]

        embed = discord.Embed(title="!Divs", color=0x7434eb)

        embed.add_field(name="Rank", value=rank+1, inline=True)
        embed.add_field(name="Player", value=member.name, inline=True)
        embed.add_field(name="Games Played", value=games_played, inline=True)

        return embed

    def clean_id(self, id):
        id = id.replace('>', '')
        return id.split('!')[-1]