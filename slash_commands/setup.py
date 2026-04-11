"""Setup slash command."""

import discord
from commands.setup import setup as RoleSetup
from commands.setupDB import setupDB
from div_colors import div_colours


async def setup_slash(
    ctx: discord.ApplicationContext,
    target: str = "roles",
    update: bool = False,
):
    """Setup roles or DB tables.

    target: roles|db
    update: when target=roles, creates missing roles / updates colors.
    """
    # Check if user has admin permissions
    if not ctx.author.guild_permissions.administrator:
        await ctx.respond("You do not have permission to use this command.", ephemeral=True)
        return

    target = target.lower().strip()

    if target == "db":
        db_setup = setupDB()
        try:
            await db_setup.handle([], None, None)
            embed = discord.Embed(
                title="Database Setup Complete",
                description="All database tables have been created successfully.",
                color=discord.Colour.green(),
            )
            embed.add_field(
                name="Tables Created",
                value="- leaderboard\n- games\n- users",
                inline=False,
            )
            await ctx.respond(embed=embed)
        except Exception as e:
            await ctx.respond(f"Database setup failed: {str(e)}")
        return

    if target != "roles":
        await ctx.respond("Invalid setup target. Use `roles` or `db`.")
        return

    role_setup = RoleSetup()
    roles = await ctx.guild.fetch_roles()
    role_names = [x.name for x in roles]

    if update:
        await role_setup.update_roles(role_names, ctx)
        await ctx.respond("Updated roles")
        return

    messages = []
    for gamemode in ["6's", "highlander"]:
        if f"ETF2L - Premiership {gamemode}" not in role_names:
            for name, col in list(div_colours.items())[:-2]:
                await role_setup.create_role(ctx, name + " " + gamemode, col)

            for name, col in list(div_colours.items())[:-2]:
                if name not in role_names:
                    await role_setup.create_role(ctx, name, col)

            messages.append(f"{gamemode} roles have been added")
        else:
            messages.append(
                "This server already has the required roles for {}".format(gamemode)
            )

    await ctx.respond("\n".join(messages))
