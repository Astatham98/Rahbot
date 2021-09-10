from autobalance import getRanks
import discord


def return_ranks_embed(members, message):
    divs = {}
    skill_divs = {}
    for member in members:
        roles = member.roles
        div = getRanks.get_region_roles(roles, message)
        skill = getRanks.get_skill(div)

        divs[member] = div
        skill_divs[member] = skill

    skill_divs = dict(sorted(skill_divs.items(), key=lambda item: item[1], reverse=True))
    return create_embed(divs, skill_divs)


def create_embed(div_dict, skill_dict):
    embed = discord.Embed(title="!Divs", color=0x11ff00)
    team1_text = '\n'.join([x.name for x in list(div_dict.keys())])
    team2_text = '\n'.join([div_dict.get(x) for x in list(skill_dict.keys())])

    embed.add_field(name="Team 1", value=team1_text, inline=True)
    embed.add_field(name="Team 2", value=team2_text, inline=True)

    return embed
