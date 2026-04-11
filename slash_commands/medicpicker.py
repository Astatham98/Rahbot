"""Medic picker slash command."""

import discord
from database import Database
import random


async def medicpicker_slash(ctx: discord.ApplicationContext, player: discord.Member = None):
    """Pick a medic from your last game or (admin) set immunity for a player."""
    db = Database()

    if player:
        # Grant immunity (admin only)
        if not ctx.author.guild_permissions.administrator:
            await ctx.respond("Only admins can grant immunity.", ephemeral=True)
            return

        db.set_immune(str(player.id))
        await ctx.respond(
            f"{player.nick if player.nick else player.name} has been given immunity."
        )
        return

    # Find team members from last game
    team = [x[0] for x in db.find_teammates(str(ctx.author.id)) if x[0] != ""]

    if not team:
        await ctx.respond("Unable to find the corresponding team.")
        return

    # Filter out immune players
    guild = ctx.guild
    available_players = []

    for player_id in team:
        try:
            member = guild.get_member(int(player_id))
            if member:
                available_players.append(member)
        except Exception:
            pass

    if not available_players:
        await ctx.respond("No players available to pick as medic.")
        return

    # Pick a random player
    chosen_player = random.choice(available_players)

    # Give immunity to the chosen player
    db.set_immune(str(chosen_player.id))

    # Show who was picked
    user_names = [p.nick if p.nick else p.name for p in available_players]

    await ctx.respond(
        'Choosing a medic from: {}\n{} has been selected to play medic.'.format(
            ", ".join(user_names),
            chosen_player.nick if chosen_player.nick else chosen_player.name,
        )
    )
