"""Rank slash command."""

import discord
from database import Database


async def rank_slash(ctx: discord.ApplicationContext, player: discord.Member = None):
    """Show player rank based on games played in the leaderboard database."""
    db = Database()
    ids, _, played = db.get_players_and_games_played()

    target = player or ctx.author

    try:
        rank = ids.index(str(target.id))
        games_played = played[rank]

        embed = discord.Embed(title="Rank", color=0x7434EB)
        embed.add_field(name="Rank", value=rank + 1, inline=True)
        embed.add_field(name="Player", value=target.display_name, inline=True)
        embed.add_field(name="Games Played", value=games_played, inline=True)
    except ValueError:
        embed = discord.Embed(title="WARNING", color=0xFC0303)
        embed.add_field(
            name="User not recognized",
            value="This user is currently not in the database - play a pug to get a rank",
            inline=True,
        )

    await ctx.respond(embed=embed)
