"""Rank slash command."""

import discord
from discord.ext import commands
import utils


async def rank_slash(ctx: discord.ApplicationContext, player: discord.Member = None):
    """Show player rank information.
    
    Parameters
    ----------
    player: discord.Member
        Player to check rank for (default: yourself)
    """
    await ctx.defer()
    
    target = player or ctx.author
    
    roles = [role.name for role in target.roles]
    
    embed = discord.Embed(
        title=f"📊 Rank for {target.display_name}",
        color=discord.Colour.blue()
    )
    
    # Filter for division roles
    divisions = []
    for role in roles:
        if any(region in role.lower() for region in [
            "etf2l", "rgl", "asia", "ozfort", "fbtf", "casual"
        ]):
            divisions.append(role)
    
    if divisions:
        embed.add_field(
            name="Current Ranks",
            value="\n".join(f"{div}" for div in divisions),
            inline=False
        )
    else:
        embed.add_field(
            name="Current Ranks",
            value="No ranked roles found. Use `/getdiv` to register your division.",
            inline=False
        )
    
    if target.joined_at:
        embed.set_footer(text=f"Member since: {target.joined_at.strftime('%Y-%m-%d')}")
    
    await ctx.respond(embed=embed)
