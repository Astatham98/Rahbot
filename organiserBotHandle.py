from autobalance import mentionByRank
from autobalance import autobalance
import settings
from database_sqlite import Database
from readyup.getServerFromEmbed import mapMessageHandler
import re


class OrganiserBotHandle:
    def __init__(self, embed=None, message=None, client=None):
        self.client = client
        self.embed = embed
        self.guild = message.guild
        self.message = message
        self.db = Database()

    # If there are all the players in the pug find the members in the discord and ping them
    async def handle(self):
        true_members = []
        if (
            self.get_game_ready(self.embed)
            and self.get_game_id(self.embed) not in settings.LAST_PLAYED
        ):
            settings.LAST_PLAYED.append(self.get_game_id(self.embed))
            true_members = await self.find_members(self.guild, self.embed)
            await self.use_mention_mode(true_members)
        elif self.get_game_started(self.embed):
            game_id = self.get_game_id(self.embed)
            if game_id in settings.LAST_PLAYED:
                settings.LAST_PLAYED.remove(game_id)
                
            # Get the connect for a match
            # connectStr = await mapMessageHandler(self.embed, game_id)
            # await self.message.channel.send(connectStr)
            
            game_members = await self.get_teams(self.embed)
            # Add players to the leaderboard if the game has started
            for member in game_members:
                member = self.guild.get_member(int(member))
                self.db.insert_into_leaderboard(member)

    # Find the total number of players added
    def get_game_ready(self, embed):
        try:
            compare = ["is now on the draft stage!", "is now on the check-in stage!"]
            if any(phrase in embed.title.lower() for phrase in compare):
                return True
            return False
        except Exception:
            return False

    def get_game_started(self, embed):
        try:
            if "has started!" in embed.title:
                return True
            return False
        except AttributeError:
            return False

    # Find the members in the discord and mentions them in some form
    async def find_members(self, guild, embed):
        members = []
        ids = self.get_member_names_check_in(embed)

        for user_id in ids:
            member = guild.get_member(int(user_id))
            if member:
                members.append(member)
        return members

    async def get_teams(self, embed):
        red = [
            self.parse_mention(x.strip()) for x in embed.fields[0].value.split("\u200b")
        ][1:]
        blue = [
            self.parse_mention(x.strip()) for x in embed.fields[1].value.split("\u200b")
        ][1:]
        ID = self.get_game_id(embed)

        [self.db.games(player, ID, "red") for player in red]
        [self.db.games(player, ID, "blue") for player in blue]

        return red + blue

    def parse_mention(self, mention: str):
        """turns a mention into an id string"""
        if re.match(r"`〈[A-Z]〉`", mention):
            mention = re.split(r"`〈[A-Z]〉`", mention)[1].strip()

        id = mention.replace(">", "")
        id = id.replace("<@!", "")
        id = id.replace("<@", "")
        return id

    async def use_mention_mode(self, true_members):
        if settings.MENTION_MODE == 0:
            # Mention mode auto balances teams
            balanced = autobalance.autobalance(true_members, self.message)
            await self.message.channel.send(embed=balanced)
        elif settings.MENTION_MODE == 1:
            # Mention mode returns players ranked by their dic
            by_rank = mentionByRank.return_ranks_embed(true_members)
            await self.message.channel.send(embed=by_rank)

    def get_game_id(self, embed):
        if hasattr(embed, "footer") and embed.footer:
            footer = embed.footer.text
            footer_split = footer.split(" ")  # Gets the footer and splits it
            id = footer_split[-1]
            return id
        return None
    
    def get_member_names(self, embed):
        members = [
            embed.fields[0].value.split("`")[1],
            embed.fields[1].value.split("`")[1],
        ]
        print(f"Members in member_names: {members}") # Debug for real game
        rest = embed.fields[2].value.split("`")[1:]
        members += rest[::2]
        print(f"Rest in member_names: {rest}")

        return [self.parse_mention(x) for x in members if x]
    
    def get_member_names_check_in(self, embed):
        members = []
        
        members += [x.strip() for x in embed.fields[0].value.split("\u200b")]

        return [self.parse_mention(x) for x in members if x]

