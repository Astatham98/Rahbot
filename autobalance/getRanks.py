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
def get_region_roles(roles):
    return get_role_and_region(roles, "6's")
       

# Goes through a users roles and finds one that meets the requirements
def get_roles(region, roles, gamemode):
    for role in roles:
        if region in role.name and gamemode in role.name:
            return parse_role(role.name)

def get_role_and_region(roles, gamemode):
    for role in roles:
        if gamemode in role.name or gamemode.replace("'", "") in role.name:
            return parse_role(role.name), role.name.split(' ')[0]

# Parses roles and gets the div only
def parse_role(role):
    role = role.split(' ')
    return " ".join(role[2:-1])


def get_skill(role_name, region):
    if region == 'ETF2L':
        skills_nums = {
            None: 1,
            'open': 4,
            'low': 7,
            'mid': 10,
            'division 3': 11,
            'division 2': 15,
            'division 1': 18,
            'premiership': 22
        }
        return skills_nums[role_name.lower().strip()]

    elif region == 'AsiaFortress':
        skills_nums = {
            None: 1,
            'division 4': 2,
            'division 3': 5,
            'division 2': 14,
            'division 1': 19
        }
        return skills_nums[role_name.lower().strip()]

    elif region == 'OzFortress':
        skills_nums = {
            None: 1,
            'open': 1,
            'main':13,
            'intermediate': 12,
            'premier': 20
        }
        return skills_nums[role_name.lower().strip()]

    elif region == 'RGL':
        skills_nums = {
            None: 1,
            'newcomer': 3,
            'amateur': 6,
            'intermediate': 9,
            'main': 13,
            'advanced': 17,
            'invite': 21
        }
        return skills_nums[role_name.lower().strip()]