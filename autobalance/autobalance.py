from autobalance import getRanks
from autobalance import sumsplit
import discord


def autobalance(members, message):
    rank_nums = getRanks.get_ranks(members, message)
    split = sumsplit.sumSplit(list(rank_nums.values()))

    if len(list(rank_nums.values())) > 1:
        t1, t2 = split[0], split[1]
        team1, team2 = [], []
        for t in t1:
            member, rank_nums = find_member_by_skill(rank_nums, t)
            team1.append(member)
        for t in t2:
            member, rank_nums = find_member_by_skill(rank_nums, t)
            team2.append(member)

        return generate_embed(team1, team2)


def find_member_by_skill(dictionary, skill):
    for k, v in dictionary.items():
        if skill == v:
            del dictionary[k]
            return k, dictionary

def generate_embed(team1, team2):
    embed=discord.Embed(title="Recommended teams", color=0x11ff00)
    team1_text = '\n'.join([x.name for x in team1])
    team2_text = '\n'.join([x.name for x in team2])

    embed.add_field(name="Team 1", value=team1_text, inline=True)
    embed.add_field(name="Team 2", value=team2_text, inline=True)
    
    return embed