from autobalance import mentionByRank
from autobalance import autobalance
import settings
from database import Database
from readyup.readyup import Ready
from readyup import closeoldstartnew as closeopen


class OrganiserBotHandle:
    def __init__(self, embed=None, message=None, client=None):
        self.client = client
        self.embed = embed
        self.guild = message.guild
        self.message = message
        self.db = Database()

    # If there are all the players in the pug find the members in the discord and ping them
    async def handle(self):
        if self.get_game_ready(self.embed) and self.get_game_id(self.embed) != settings.LAST_PLAYED:
            settings.LAST_PLAYED = self.get_game_id(self.embed)
            await self.find_members(self.guild, self.embed)

    # Find the total number of players added
    def get_game_ready(self, embed):
        try:
            if embed.title == "__**Pug** is now on the draft stage!__":
                print(embed.title)
                return True
            return False
        except AttributeError:
            return False

    # Find the members in the discord and mentions them in some form
    async def find_members(self, guild, embed):
        names = self.get_member_names(self.embed)

        members = []
        # Fetch all the guild members
        async for member in guild.fetch_members():
            if not member.bot:
                members.append(member)

        true_members = []
        # Find all the members that are in the names  or their nick name is in names
        for member in members:
            if member.name in names or member.nick in names:
                true_members.append(member)

        await self.mention_players(true_members)

    # When the pug is ready mention members and post other embeds based on the mention mode
    async def mention_players(self, true_members):
        # mentions = [x.mention for x in true_members]  # creates mentions for members
        # await self.message.channel.send(" ".join(mentions) + " Pug filled! join vc.")

        for memb in true_members:
            self.db.insert_into_leaderboard(memb)

        if settings.MENTION_MODE == 0:
            # Mention mode auto balances teams
            balanced = autobalance.autobalance(true_members, self.message)
            await self.message.channel.send(embed=balanced)
        elif settings.MENTION_MODE == 1:
            # Mention mode returns players ranked by their dic
            by_rank = mentionByRank.return_ranks_embed(true_members, self.message)
            await self.message.channel.send(embed=by_rank)

    def get_game_id(self, embed):
        footer = embed.footer.text
        footer_split = footer.split(" ")  # Gets the footer and splits it
        id = footer_split[-1]
        return id

    def get_member_names(self, embed):
        members = [embed.fields[0].value.split("`")[1], embed.fields[1].value.split("`")[1]]
        rest = embed.fields[2].value.split("`")[1:]
        members += rest[::2]

        return members
