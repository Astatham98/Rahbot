"""Edit role name slash command."""

import discord
from div_colors import div_colours


async def editrolename_slash(
    ctx: discord.ApplicationContext,
    role_name: str = None,
    new_name: str = None,
    mass: bool = False,
):
    """Rename one role or mass append a suffix to division roles (admin only)."""
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond("Insufficient rank.", ephemeral=True)
        return

    if not new_name:
        await ctx.respond("Please input the command correctly")
        return

    roles = await ctx.guild.fetch_roles()

    if not mass:
        if not role_name:
            await ctx.respond("Role name is required when mass is false.")
            return

        role = discord.utils.find(lambda x: x.name.lower() == role_name.lower(), roles)
        if role is None:
            await ctx.respond("Role not found.")
            return

        await role.edit(name=new_name)
        await ctx.respond("Role has been edited.")
        return

    div_names = [x.lower() for x in div_colours.keys()]
    discord_roles = [
        x for x in roles if x.name.lower() in div_names and x.name.lower() != "newb"
    ]
    for role in discord_roles:
        await role.edit(name=role.name + " " + new_name)

    await ctx.respond("Roles successfully mass updated")
