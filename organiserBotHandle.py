from autobalance import mentionByRank
from autobalance import autobalance
import settings


class OrganiserBotHandle:
    def __init__(self, embed=None, message=None):
        self.embed = embed
        self.guild = message.guild
        self.message = message

    async def handle(self):
        if self.get_total_players(self.embed):
            await self.find_members(self.guild, self.embed)

    def get_total_players(self, embed):
        footer = embed.footer.text
        footer_split = footer.split(" ")
        outof = footer_split[3]
        outof_split = outof.split("/")
        current, goal = outof_split[0], outof_split[1]
        return current == goal

    async def find_members(self, guild, embed):
        names = []
        if len(embed.fields) > 3:
            for field in embed.fields[-6:]:
                if field.value != "-":
                    names.append(field.value.split(" ")[-1])
        else:
            field = embed.fields[-1].value
            field_split = field.split("<:tf2_icon:882972601939537941>")
            names = [x.strip() for x in field_split[1:]]

        members = []
        async for member in guild.fetch_members():
            if not member.bot:
                members.append(member)

        true_members = []
        for member in members:
            if member.name in names or member.nick in names:
                true_members.append(member)

        mentions = [x.mention for x in true_members]
        await self.message.channel.send(" ".join(mentions) + " Pug filled! join vc.")


        if settings.MENTION_MODE == 0:
            balanced = autobalance.autobalance(true_members, self.message)
            await self.message.channel.send(embed=balanced)
        elif settings.MENTION_MODE == 1:
            by_rank = mentionByRank.return_ranks_embed(true_members, self.message)
            await self.message.channel.send(embed=by_rank)
