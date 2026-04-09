"""Get division slash command."""

import discord
from discord.ext import commands
from divgetters.etf2l_player_id_get import Etf2l
from divgetters.ozf_player_id_get import Ozfortress
from divgetters.asia_player_id_get import AsiaFortress
from divgetters.sa_player_id_get import SA
from divgetters.rgl_player_id_get import RGL
from database_sqlite import Database


async def getdiv_slash(ctx: discord.ApplicationContext, profile_url: str):
    """Get division role based on your player profile.
    
    Parameters
    ----------
    profile_url: str
        Your player profile URL (etf2l.org, rgl.gg, match.tf, ozfortress.com, fbtf.tf) or "casual"
    """
    await ctx.defer()
    
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
        await ctx.respond("Invalid profile URL. Use your ETF2L, RGL, AsiaFortress, OzFortress, or FBTF profile.")
        return
    
    roles = await ctx.guild.fetch_roles()
    
    # Check if user exists
    exist_and_same, no_users = db.check_user_exists(str(ctx.author.id), link)
    
    if no_users or exist_and_same:
        # Get steam ID if possible
        steam = "None"
        if "etf2l" in link:
            steam = Etf2l.get_steam(link)
            
        # Insert user into database
        try:
            db.insert_into_users(str(ctx.author.id), link, steam, False)
        except Exception:
            pass
            
        # Check for bans
        banned = False
        if "etf2l" in link:
            banned = Etf2l.get_banned(link)
            
        if banned:
            divs = ["banned"]
            
        # Find the newb role
        newb_role = discord.utils.get(roles, name="newb")
        if newb_role:
            await ctx.author.remove_roles(newb_role)
            
        # Remove existing division roles for this region
        if len(divs) > 0 and len(divs[0].split(" ")) > 1:
            region = divs[0].split(" ")[0].lower()
            for role in ctx.author.roles:
                if region in role.name.lower():
                    await ctx.author.remove_roles(role)
                    
        # Assign the new role
        success = False
        for div in divs:
            role = discord.utils.find(
                lambda r: r.name.lower().replace(" ", "") == div.lower().replace(" ", ""),
                roles
            )
            if role:
                await ctx.author.add_roles(role)
                await ctx.respond(f"✅ {ctx.author.mention} has been given the **{div}** role.")
                success = True
                break
                
        if not success:
            await ctx.respond("Valid profile, but no matching role found for your division.")
    else:
        await ctx.respond("This profile is already registered to another user.")
