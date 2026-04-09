"""Get server slash command."""

import discord
from discord.ext import commands
from getserver import get_server


async def getserver_slash(ctx: discord.ApplicationContext):
    """Get a reserved server for your game."""
    await ctx.defer()
    
    try:
        server = get_server("pl_badwater", "eu")
        
        if server:
            embed = discord.Embed(
                title="🎮 Server Reserved",
                color=discord.Colour.green()
            )
            embed.add_field(
                name="Server Details",
                value=f"**IP:** `{server.get('ip', 'N/A')}`\n"
                      f"**Port:** `{server.get('port', 'N/A')}`\n"
                      f"**Password:** `{server.get('password', 'N/A')}`",
                inline=False
            )
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("No servers are currently available. Please try again later.")
            
    except Exception as e:
        await ctx.respond(f"Failed to get server: {str(e)}")
