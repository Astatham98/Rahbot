"""Leaderboard slash command."""

import discord
from database_sqlite import Database
from pagination import ButtonPaginationView


def build_pages(names, played, items_per_page=25):
    pages = []
    for start in range(0, len(names), items_per_page):
        end = start + items_per_page
        pages.append((names[start:end], played[start:end], start, len(names)))

    if len(pages) == 0:
        pages.append(([], [], 0, 0))

    return pages


def create_embed(page_data, page_index=0, total_pages=1):
    page_names, page_played, start, total_players = page_data

    embed = discord.Embed(title="Leaderboard*", color=0x7434EB)
    rank_text = "\n".join([str(start + x + 1) for x in range(len(page_names))])
    player_text = "\n".join(page_names)
    played_text = "\n".join([str(x) for x in page_played])

    embed.add_field(name="Rank", value=rank_text or "-", inline=True)
    embed.add_field(name="Player", value=player_text or "-", inline=True)
    embed.add_field(name="Games Played", value=played_text or "-", inline=True)
    embed.set_footer(
        text=f"Page {page_index + 1}/{total_pages} | Total players: {total_players}"
    )
    return embed


async def leaderboard_slash(
    ctx: discord.ApplicationContext,
    page: int = 1,
    player: discord.Member = None,
):
    """Show the games played leaderboard or a specific player's leaderboard position."""
    db = Database()
    ids, names, played = db.get_players_and_games_played()

    if player is not None:
        try:
            rank = ids.index(str(player.id))
            games_played = played[rank]

            embed = discord.Embed(title="Leaderboard", color=0x7434EB)
            embed.add_field(name="Rank", value=rank + 1, inline=True)
            embed.add_field(name="Player", value=player.display_name, inline=True)
            embed.add_field(name="Games Played", value=games_played, inline=True)
        except ValueError:
            embed = discord.Embed(title="WARNING", color=0xFC0303)
            embed.add_field(
                name="User not recognized",
                value="This user is currently not in the database",
                inline=True,
            )

        await ctx.respond(embed=embed)
        return

    pages = build_pages(names, played)
    view = ButtonPaginationView(pages, create_embed, ctx.author.id)

    if len(pages) > 0:
        clamped_page = max(1, min(page, len(pages)))
        view.current_page = clamped_page - 1
        view._update_buttons()

    await ctx.respond(embed=view.current_embed(), view=view)

    # Best-effort attachment for timeout button disabling.
    try:
        original_msg = await ctx.interaction.original_response()
        view.message = original_msg
    except Exception:
        pass
