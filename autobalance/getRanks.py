# For all members get their division as a skill number and put it in a dictionary
def get_ranks(members, message):
    skill_ranks = {}
    for member in members:
        roles = member.roles
        div_name, region = get_region_roles(roles, message)  # Gets the role based on the region the channel is in
        div_num = get_skill(div_name)  # Converts string div role into a skill num
        skill_ranks[member] = div_num

    return skill_ranks


# Gets the get_role based on the location of the channel name
def get_region_roles(roles, message):
    channel = message.channel.name
    if "eu" in channel.lower():
        return get_roles('ETF2L', roles, "6's"), 'ETF2L'
    if "asia" in channel.lower():
        return get_roles('AsiaFortress', roles, "6's"), 'AsiaFortress'
    if "ozfort" in channel.lower():
        return get_roles('OzFortress', roles, "6's"), 'OzFortress'
    if 'na' in channel.lower():
        return get_roles('RGL', roles, "6s"), 'RGL'


# Goes through a users roles and finds one that meets the requirements
def get_roles(region, roles, gamemode):
    for role in roles:
        if region in role.name and gamemode in role.name:
            return parse_role(role.name)


# Parses roles and gets the div only
def parse_role(role):
    role = role.split(' ')
    return " ".join(role[2:-1])


def get_skill(role_name, region):
    if region == 'ETF2L':
        skills_nums = {
            None: 1,
            'open': 1,
            'low': 2,
            'mid': 3,
            'division 3': 4,
            'division 2': 5,
            'division 1': 6,
            'premiership': 7
        }
        return skills_nums[role_name.lower().strip()]

    elif region == 'AsiaFortress':
        skills_nums = {
            None: 1,
            'division 4': 1,
            'division 3': 2,
            'division 2': 3,
            'division 1': 4
        }
        return skills_nums[role_name.lower().strip()]

    elif region == 'OzFortress':
        skills_nums = {
            None: 1,
            'open': 1,
            'main': 2,
            'intermediate': 3,
            'premier': 4
        }
        return skills_nums[role_name.lower().strip()]

    elif region == 'RGL':
        skills_nums = {
            None: 1,
            'newcomer': 1,
            'amateur': 2,
            'intermediate': 3,
            'main': 4,
            'advanced': 5,
            'invite': 6
        }
        return skills_nums[role_name.lower().strip()]