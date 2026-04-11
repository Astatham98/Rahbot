"""Get user account details slash command."""

import re
import discord
from database_sqlite import Database
import utils


async def getuseraccounts_slash(ctx: discord.ApplicationContext, query: str):
    """Get linked account details by mention, ETF2L URL, or Steam profile/ID."""
    db = Database()
    query_type = None
    lookup_query = query.strip()

    if "@" in lookup_query:
        lookup_query = utils.parse_mention(lookup_query)
        query_type = "id"
    elif "etf2l" in lookup_query.lower():
        query_type = "linkedProfile"
    else:
        replaced_query = lookup_query.replace("https://steamcommunity.com", "")
        pattern = (
            r"(?P<CUSTOMPROFILE>https?\:\/\/steamcommunity\.com\/id\/[A-Za-z_0-9]+)"
            r"|(?P<CUSTOMURL>\/id\/[A-Za-z_0-9]+)"
            r"|(?P<PROFILE>https?\:\/\/steamcommunity.com\/profiles\/[0-9]+)"
            r"|(?P<STEAMID2>STEAM_[10]\:[10]\:[0-9]+)"
            r"|(?P<STEAMID3>\[U\:[10]\:[0-9]+\])"
            r"|(?P<STEAMID64>[^\/][0-9]{8,})"
        )
        is_steam = re.match(pattern, replaced_query)
        if is_steam:
            query_type = "steam"

    if query_type is None:
        await ctx.respond("Invalid user")
        return

    user_details = db.get_user_accounts(query_type, lookup_query)
    if user_details is None:
        await ctx.respond("No user details found for this query.")
        return

    discord_user = ctx.bot.get_user(int(user_details[0]))
    if discord_user is None:
        try:
            discord_user = await ctx.bot.fetch_user(int(user_details[0]))
        except Exception:
            discord_user = None

    username = discord_user.display_name if discord_user else str(user_details[0])
    linked_profile = user_details[1]
    steam = user_details[2]
    registered_date = user_details[3]
    verified = user_details[4]

    embed = discord.Embed(title=username, colour=discord.Colour.blue())
    text = (
        f"Profile: {linked_profile}\n"
        f"Steam: {steam}\n"
        f"Date Registered: {registered_date}\n"
        f"Verified: {verified}"
    )
    embed.add_field(name="Details", value=text, inline=True)
    await ctx.respond(embed=embed)
