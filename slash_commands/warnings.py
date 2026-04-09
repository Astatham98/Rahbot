"""Warnings slash command."""

import discord
from discord.ext import commands
from database_sqlite import Database


async def warnings_slash(
    ctx: discord.ApplicationContext,
    player: discord.Member = None,
    duration: str = None,
    reason: str = None
):
    """Manage player warnings.
    
    Parameters
    ----------
    player: discord.Member
        Player to warn or view warnings for
    duration: str
        Warning duration (e.g. 1h, 3d, 1w, permanent)
    reason: str
        Reason for the warning
    """
    await ctx.defer()
    
    db = Database()
    
    # Check if user has admin permissions
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond("You do not have permission to use this command.", ephemeral=True)
        return
    
    # No player provided - show help
    if not player:
        embed = discord.Embed(
            title="Warnings Command Help",
            description="Manage player warnings",
            color=discord.Colour.orange()
        )
        embed.add_field(
            name="View warnings",
            value="`/warnings @Player` - View all warnings for a player",
            inline=False
        )
        embed.add_field(
            name="Issue warning",
            value="`/warnings @Player 2h \"Spamming chat\"`\n"
                  "Valid durations: 1h, 2h, 6h, 12h, 1d, 3d, 1w, permanent",
            inline=False
        )
        await ctx.respond(embed=embed)
        return
    
    # View existing warnings
    if not duration or not reason:
        warnings = db.get_warned_player(str(player.id))
        
        embed = discord.Embed(
            title=f"Warnings for {player.display_name}",
            color=discord.Colour.orange()
        )
        
        if warnings:
            for i, warning in enumerate(warnings, 1):
                duration = f"{warning[1]} minutes"
                embed.add_field(
                    name=f"Warning #{i}",
                    value=f"Duration: **{duration}**\nReason: {warning[2]}",
                    inline=False
                )
        else:
            embed.description = "No active warnings for this player."
            
        await ctx.respond(embed=embed)
        return
    
    # Issue new warning
    try:
        # Convert duration to minutes
        import re
        
        if duration.lower() == "permanent":
            conv_dur = 525600*10  # 10 year in minutes
            readable = "Permanent"
        else:
            match = re.match(r'^(\d+)([hdw])$', duration.lower())
            if not match:
                await ctx.respond("Invalid duration format. Use: 1h, 3d, 1w, permanent")
                return
                
            num = int(match.group(1))
            unit = match.group(2)
            
            if unit == 'h':
                conv_dur = num * 60
                readable = f"{num} hour(s)"
            elif unit == 'd':
                conv_dur = num * 1440
                readable = f"{num} day(s)"
            elif unit == 'w':
                conv_dur = num * 10080
                readable = f"{num} week(s)"
        
        db.warn_player(str(player.id), conv_dur, reason)
        
        await ctx.respond(
            f"**{player.mention}** has been warned for **{readable}**\n"
            f"Reason: {reason}"
        )
        
    except Exception as e:
        await ctx.respond(f"Failed to issue warning: {str(e)}")
