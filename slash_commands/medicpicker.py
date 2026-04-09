"""Medic picker slash command."""

import discord
from discord.ext import commands
from database_sqlite import Database
import random


async def medicpicker_slash(ctx: discord.ApplicationContext, player: discord.Member = None):
    """Pick a medic from your last game or set immunity.
    
    Parameters
    ----------
    player: discord.Member
        Player to grant immunity (optional - admin only)
    """
    await ctx.defer()
    
    db = Database()
    
    if player:
        # Grant immunity (admin only)
        if not ctx.author.guild_permissions.administrator:
            await ctx.respond("Only admins can grant immunity.", ephemeral=True)
            return
            
        db.set_immune(str(player.id))
        await ctx.respond(f"{player.mention} has been granted immunity.")
    
    # Find team members from last game
    team = [x[0] for x in db.find_teammates(str(ctx.author.id)) if x[0] != ""]
    
    if not team:
        await ctx.respond("Could not find your last game team.")
        return
        
    # Filter out immune players
    guild = ctx.guild
    available_players = []
    
    for player_id in team:
        try:
            member = guild.get_member(int(player_id))
            if member:
                available_players.append(member)
        except:
            pass
    
    if not available_players:
        await ctx.respond("No players available to pick as medic.")
        return
        
    # Pick a random player
    chosen_player = random.choice(available_players)
    
    # Give immunity to the chosen player
    db.set_immune(str(chosen_player.id))
    
    # Show who was picked
    player_names = [p.display_name for p in available_players]
    
    embed = discord.Embed(
        title="⚕️ Medic Selected",
        color=discord.Colour.blue()
    )
    embed.add_field(
        name="Available Players",
        value=", ".join(player_names),
        inline=False
    )
    embed.add_field(
        name="Selected Medic",
        value=f"**{chosen_player.mention}** has been selected to play medic!",
        inline=False
    )
    
    await ctx.respond(embed=embed)
