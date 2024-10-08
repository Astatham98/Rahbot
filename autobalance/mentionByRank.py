from autobalance import getRanks
import discord


# Returns an embed of users and their divisions
def return_ranks_embed(members):
    divs = {}
    skill_divs = {}
    region_dict = {}
    # for each members add to a dictionary with {member: div} and {member: skill{
    for member in members:
        print(member)
        roles = member.roles
        div, region = getRanks.get_region_roles(roles)  # Gets the users text div
        skill = getRanks.get_skill(div, region)  # gets the users skill number

        divs[member] = div
        skill_divs[member] = skill
        region_dict[member] = get_shortened(region)

    # Sorts the skill dict from largest to smallest
    skill_divs = dict(
        sorted(skill_divs.items(), key=lambda item: item[1], reverse=True)
    )
    return create_embed(divs, skill_divs, region_dict)


# Creates an embed based on the ranked skill to show player and div
def create_embed(div_dict, skill_dict, region_dict):
    embed = discord.Embed(title="!Divs", color=0x11FF00)
    team1_text = "\n".join(
        [x.nick if x.nick else x.name for x in list(skill_dict.keys())]
    )  # users names on a newline
    team2_text = "\n".join(
        [div_dict.get(x) for x in list(skill_dict.keys())]
    )  # Users text div
    team3_text = "\n".join(
        [region_dict.get(x) for x in list(skill_dict.keys())]
    )  # Users text div

    embed.add_field(name="Player", value=team1_text, inline=True)
    embed.add_field(name="Div", value=team2_text, inline=True)
    embed.add_field(name="Region", value=team3_text, inline=True)

    return embed


def get_shortened(region):
    regions = {"AsiaFortress": "Asia", "OzFortress": "OzFort", None: "Unknown"}

    return regions.get(region, region)
