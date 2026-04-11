"""Run DB maintenance slash command."""

import discord
from database import Database


async def rundb_slash(
    ctx: discord.ApplicationContext,
    action: str,
    player: discord.Member,
    amount: int = None,
):
    """Admin DB maintenance: reset, set_played, remove."""
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond("Insufficient rank.", ephemeral=True)
        return

    db = Database()
    action = action.lower().strip()

    if action not in ["reset", "set_played", "remove"]:
        await ctx.respond("Incorrect input")
        return

    if action == "reset":
        db.modify_player(str(player.id), 0)
        await ctx.respond(f"Reset games played for {player.display_name}.")
        return

    if amount is None:
        await ctx.respond("Amount is required for this action.")
        return

    if action == "set_played":
        db.modify_player(str(player.id), amount)
        await ctx.respond(
            f"Set games played for {player.display_name} to {amount}."
        )
        return

    db.modify_player(str(player.id), amount, True)
    await ctx.respond(
        f"Removed {amount} games from {player.display_name}."
    )
