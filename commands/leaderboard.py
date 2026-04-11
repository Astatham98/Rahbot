from commands.base_command import BaseCommand
from database_sqlite import Database
import discord
from pagination import ButtonPaginationView


class Leaderboard(BaseCommand):
    def __init__(self):
        self.db = Database()
        description = "Returns a leaderboard."
        params = None
        super().__init__(description, params)

    async def handle(self, params, message, client):
        db = self.db
        id, name, played = db.get_players_and_games_played()

        if len(params) > 0:
            member_id = self.clean_id(params[0])
            player = client.get_user(int(member_id))
            embed = self.get_player_rank(player, id, played)
            await message.channel.send(embed=embed)
        else:
            pages = self.build_pages(name, played)
            view = ButtonPaginationView(pages, self.create_embed, message.author.id)
            embed = view.current_embed()
            sent_msg = await message.channel.send(embed=embed, view=view)
            view.message = sent_msg

    def build_pages(self, names, played):
        pages = []
        for start in range(0, len(names), 25):
            end = start + 25
            pages.append((names[start:end], played[start:end], start))

        if len(pages) == 0:
            pages.append(([], [], 0))

        return pages

    def create_embed(self, page_data, page_index=0, total_pages=1):
        names, played, base_index = page_data
        embed = discord.Embed(title="Leaderboard*", color=0x7434EB)
        team1_text = "\n".join(names)
        team2_text = "\n".join([str(x) for x in played])
        page_len = len(names)
        rank = "\n".join([str(base_index + x + 1) for x in range(page_len)])

        embed.add_field(name="Rank", value=rank if rank else "-", inline=True)
        embed.add_field(
            name="Player", value=team1_text if team1_text else "-", inline=True
        )
        embed.add_field(
            name="Games Played", value=team2_text if team2_text else "-", inline=True
        )
        embed.set_footer(text=f"Page {page_index + 1}/{total_pages}")

        return embed

    def get_player_rank(self, member, ids, played):
        try:
            rank = ids.index(str(member.id))
            games_played = played[rank]

            embed = discord.Embed(title="Leaderboard", color=0x7434EB)

            embed.add_field(name="Rank", value=rank + 1, inline=True)
            embed.add_field(name="Player", value=member.name, inline=True)
            embed.add_field(name="Games Played", value=games_played, inline=True)

            return embed
        except ValueError:
            embed = discord.Embed(title="WARNING", color=0xFC0303)
            embed.add_field(
                name="User not recognized",
                value="This user is currently not in the database",
                inline=True,
            )

            return embed

    def clean_id(self, id):
        id = id.replace(">", "")
        return id.split("!")[-1]
