from autobalance import getRanks
from autobalance import sumsplit
import discord

# Autobalances teams  based on a list of members
def autobalance(members, message):
    rank_nums = getRanks.get_ranks(members, message) # Gets a members rank in a skill number
    split = sumsplit.sumSplit(list(rank_nums.values()))
    # Uses an recursive algorithm to split the teams into two similar sums based on their skill numbers

    if len(list(rank_nums.values())) > 1:
        t1, t2 = split[0], split[1]
        team1, team2 = [], []
        # Goes through the team skill rank and find a player with that skill number
        for t in t1:
            member, rank_nums = find_member_by_skill(rank_nums, t)
            team1.append(member)
        for t in t2:
            member, rank_nums = find_member_by_skill(rank_nums, t)
            team2.append(member)

        return generate_embed(team1, team2)

# Returns the members and a popped dictionary if the members skill rank is our desired skill
def find_member_by_skill(dictionary, skill):
    for k, v in dictionary.items():
        if skill == v:
            del dictionary[k]
            return k, dictionary

# Generates and embed of recommended teams based on 2 lists of members
def generate_embed(team1, team2):
    embed=discord.Embed(title="Recommended teams", color=0x11ff00)
    team1_text = '\n'.join([x.name for x in team1])
    team2_text = '\n'.join([x.name for x in team2])

    embed.add_field(name="Team 1", value=team1_text, inline=True)
    embed.add_field(name="Team 2", value=team2_text, inline=True)
    
    return embed