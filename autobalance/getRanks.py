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
            'open': 1,
            'low': 2,
            'mid': 3,
            'division 3': 3,
            'division 2': 4,
            'division 1': 5,
            'premiership': 6
        }
        return skills_nums[role_name.lower().strip()]

    elif region == 'AsiaFortress':
        skills_nums = {
            None: 1,
            'division 4': 1,
            'division 3': 2,
            'division 2': 3,
            'division 1': 6
        }
        return skills_nums[role_name.lower().strip()]

    elif region == 'OzFortress':
        skills_nums = {
            None: 1,
            'open': 1,
            'main':3,
            'intermediate': 4,
            'premier': 6
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