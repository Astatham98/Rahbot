"""Get division slash command."""

import asyncio
import discord
from divgetters.etf2l_player_id_get import Etf2l
from divgetters.ozf_player_id_get import Ozfortress
from divgetters.asia_player_id_get import AsiaFortress
from divgetters.sa_player_id_get import SA
from divgetters.rgl_player_id_get import RGL
from database import Database


async def getdiv_slash(ctx: discord.ApplicationContext, profile_url: str):
    """Get division role based on your player profile."""
    db = Database()
    link = profile_url.strip()

    # Get division from profile
    if "etf2l" in link:
        divs = Etf2l().get_div(link)
    elif "rgl" in link:
        divs = RGL().get_div(link)
    elif "match.tf" in link:
        divs = AsiaFortress().get_div(link)
    elif "ozfortress" in link:
        divs = Ozfortress().get_div(link)
    elif "ugc" in link:
        divs = ["ugc"]
    elif "fbtf" in link:
        divs = SA().get_div(link)
    elif "casual" in link.lower():
        divs = ["casual"]
    else:
        await ctx.respond(
            "Invalid profile URL. Use your ETF2L, RGL, AsiaFortress, OzFortress, or FBTF profile."
        )
        return

    roles = await ctx.guild.fetch_roles()

    # Check if user exists
    exist_and_same, no_users = db.check_user_exists(str(ctx.author.id), link)

    if not (no_users or exist_and_same):
        await ctx.respond("This profile is already registered to another user.")
        return

    steam = Etf2l.get_steam(link) if "etf2l" in link else "None"

    try:
        db.insert_into_users(str(ctx.author.id), link, steam, False)
    except Exception:
        pass

    db.ensure_player_in_leaderboard(str(ctx.author.id), ctx.author.name)

    if "etf2l" in link and Etf2l.get_banned(link):
        divs = ["banned"]

    newb_role = discord.utils.find(lambda r: r.name.lower() == "newb", roles)
    if newb_role:
        await ctx.author.remove_roles(newb_role)

    if len(divs) > 0 and len(divs[0].split(" ")) > 1:
        region = divs[0].split(" ")[0].lower()
        for role in ctx.author.roles:
            if region in role.name.lower():
                await ctx.author.remove_roles(role)

    assigned = []
    for div in divs:
        role = discord.utils.find(
            lambda r: r.name.lower().replace(" ", "") == div.lower().replace(" ", ""),
            roles,
        )
        if role:
            await ctx.author.add_roles(role)
            assigned.append(div)

    if not assigned:
        await ctx.respond("This is not a valid role type, please try again")
        return

    await ctx.respond(
        "{} has been given the {} role.".format(ctx.author.mention, ", ".join(assigned))
    )

    await asyncio.sleep(1)
    try:
        await ctx.channel.purge()
        await welcome_message_embed(ctx)
    except Exception:
        pass


async def welcome_message_embed(ctx):
    embed = discord.Embed(
        title="Step up and get your div here!",
        description="Type /getdiv {your region profile here}",
        color=0x00D9FF,
    )
    embed.add_field(
        name="EU", value="/getdiv https://etf2l.org/forum/user/109984/", inline=False
    )
    embed.add_field(
        name="NA",
        value="/getdiv https://rgl.gg/Public/PlayerProfile.aspx?p=76561198136056704&r=40",
        inline=False,
    )
    embed.add_field(
        name="OzFort", value="/getdiv https://ozfortress.com/users/2533", inline=False
    )
    embed.add_field(
        name="Asia", value="/getdiv https://match.tf/users/5640", inline=False
    )
    embed.add_field(name="SA", value="/getdiv https://fbtf.tf/users/788", inline=False)
    embed.add_field(name="Casual", value="/getdiv casual", inline=False)
    embed.set_footer(
        text="If you get the incorrect rank or the bot misses a rank, contact Rahmed."
    )
    await ctx.channel.send(embed=embed)
