"""Get server slash command."""

import discord
from getserver import get_server


async def getserver_slash(
    ctx: discord.ApplicationContext,
    map_choice: str,
    location: str = None,
):
    """Get a reserved server for the given map and region."""
    channel_name = getattr(ctx.channel, "name", "")
    channel_region = channel_name.split("-")[0] if channel_name else ""

    if channel_region in ("eu", "na"):
        server_loc = channel_region
    else:
        server_loc = "eu"

    if location:
        if location.lower() in ("de", "fr", "nl", "chi", "ks", "la"):
            server_loc += " " + location.lower()

    try:
        server, rcon = get_server(map_choice, server_loc)

        if server is None:
            if rcon is None:
                await ctx.respond("Please enter a valid map name")
            else:
                await ctx.respond("ERROR ACCESSING THE API")
        else:
            dm_note = ""
            try:
                dm_channel = await ctx.author.create_dm()
                await dm_channel.send(
                    "The rcon string for this server is:\n"
                    "rcon_address {}; rcon_password {}".format(
                        server.split(" ")[1].replace(";", ""), rcon
                    )
                )
                dm_note = "\nRCON details sent via DM."
            except Exception:
                dm_note = "\nUnable to send DM with RCON details."

            await ctx.respond("Server IP is:\n{}{}".format(server, dm_note))
    except Exception as e:
        await ctx.respond(f"Failed to get server: {str(e)}")
