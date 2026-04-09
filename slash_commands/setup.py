"""Setup slash command."""

import discord
from discord.ext import commands
from commands.setupDB import setupDB
import settings


async def setup_slash(ctx: discord.ApplicationContext):
    """Setup bot database tables."""
    # Check if user has admin permissions
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond("You do not have permission to use this command.", ephemeral=True)
        return
    
    await ctx.defer()
    
    # Create database tables
    db_setup = setupDB()
    
    try:
        # Run setup
        db_setup.handle(None, ctx.message, None)
        
        embed = discord.Embed(
            title="Database Setup Complete",
            description="All database tables have been created successfully.",
            color=discord.Colour.green()
        )
        embed.add_field(
            name="Tables Created",
            value="- leaderboard\n- games\n- users\n- warnings",
            inline=False
        )
        
        await ctx.respond(embed=embed)
        
    except Exception as e:
        await ctx.respond(f"Database setup failed: {str(e)}")
