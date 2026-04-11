"""Warnings slash command."""

import re
import discord
from database_sqlite import Database


def convert_duration(duration):
    conv_dur = 1440
    readable = "24 hours"

    if duration is None:
        return conv_dur, readable

    duration = duration.lower().strip()
    if duration in ("p", "perma", "permanent"):
        return 526000 * 5, "5 years"

    match = re.match(r"^(\d+)([a-z]+)$", duration)
    if not match:
        raise ValueError("Invalid duration format")

    duration_time = int(match.group(1))
    time_val = match.group(2)

    if time_val in ("h", "hour", "hours"):
        conv_dur = duration_time * 60
        readable = f"{duration_time} hour(s)"
    elif time_val in ("d", "day", "days"):
        conv_dur = duration_time * 1440
        readable = f"{duration_time} day(s)"
    elif time_val in ("m", "min", "mins", "minute", "minutes"):
        conv_dur = duration_time
        readable = f"{duration_time} minute(s)"
    elif time_val in ("w", "week", "weeks"):
        conv_dur = duration_time * 1440 * 7
        readable = f"{duration_time} week(s)"
    elif time_val in ("mo", "month", "months"):
        conv_dur = duration_time * 43800
        readable = f"{duration_time} month(s)"
    elif time_val in ("s", "sec", "secs", "second", "seconds"):
        conv_dur = max(1, int(duration_time * (1 / 60)))
        readable = f"{duration_time} second(s)"
    else:
        raise ValueError("Invalid duration format")

    return conv_dur, readable


async def warnings_slash(
    ctx: discord.ApplicationContext,
    mode: str,
    player: discord.Member = None,
    duration: str = None,
    reason: str = None,
):
    """Manage player warnings with explicit get/give mode."""

    # Check if user has admin permissions
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond("You do not have permission to use this command.", ephemeral=True)
        return

    db = Database()
    
    command_type = mode.lower()
    if command_type not in ("get", "give"):
        await ctx.respond("Incorrect parameter input")
        return

    if not player:
        await ctx.respond("Player is required.")
        return

    if command_type == "get":
        warnings = db.get_warned_player(str(player.id))
        embed = discord.Embed(
            title=player.display_name,
            colour=discord.Colour.dark_orange(),
        )

        if warnings:
            text = ""
            for warning in warnings:
                text += f"banned for {warning[1]} minutes for: {warning[2]}\n "
        else:
            text = "No warnings found."

        embed.add_field(name="Warnings", value=text, inline=True)
        await ctx.respond(embed=embed)
        return

    try:
        conv_dur, readable = convert_duration(duration)
        db.warn_player(str(player.id), conv_dur, reason)

        await ctx.respond(
            f"{player.display_name} has been logged in the database as warned for {readable}"
        )
    except ValueError:
        await ctx.respond("Invalid duration format.")
