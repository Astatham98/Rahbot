"""Leaderboard slash command."""

import discord
from discord.ext import commands
from database_sqlite import Database
import settings


async def leaderboard_slash(ctx: discord.ApplicationContext, page: int = 1):
    """Show the games played leaderboard.
    
    Parameters
    ----------
    page: int
        Page number to display (default: 1)
    """
    await ctx.defer()
    
    db = Database()
    
    ids, names, played = db.get_players_and_games_played()
    
    embed = discord.Embed(
        title="🏆 Leaderboard",
        description="Players ranked by games played",
        color=discord.Colour.gold()
    )
    
    items_per_page = 10
    total_pages = (len(names) + items_per_page - 1) // items_per_page
    
    # Adjust page if out of bounds
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages
    
    start = (page - 1) * items_per_page
    end = start + items_per_page
    
    for i in range(start, min(end, len(names))):
        rank = i + 1
        
        # Medal emojis for top 3
        if rank == 1:
            medal = "🥇"
        elif rank == 2:
            medal = "🥈"
        elif rank == 3:
            medal = "🥉"
        else:
            medal = f"**{rank}.**"
            
        embed.add_field(
            name=f"{medal} {names[i]}",
            value=f"Played: **{played[i]}** games",
            inline=False
        )
    
    embed.set_footer(text=f"Page {page}/{total_pages} | Total players: {len(names)}")
    
    await ctx.respond(embed=embed)
