"""Mention mode slash command."""

import discord
import settings


async def mentionmode_slash(ctx: discord.ApplicationContext, mode: int = None):
    """Get or set mention mode (admin only)."""
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond("Insufficient rank.", ephemeral=True)
        return

    if mode is None:
        await ctx.respond(f"Mention mode is currently set to {settings.MENTION_MODE}.")
        return

    if mode not in [0, 1]:
        await ctx.respond("Incorrect input")
        return

    settings.MENTION_MODE = mode
    await ctx.respond(f"Mention mode is now set to {settings.MENTION_MODE}.")
