def get_ranks(members, message):
    skill_ranks = {}
    for member in members:
        roles = member.roles
        div_name = get_region_roles(roles, message)
        div_num = get_skill(div_name)
        skill_ranks[member] = div_num

    return skill_ranks


def get_region_roles(roles, message):
    channel = message.channel.name
    if "eu" in channel.lower():
        return get_roles('ETF2L', roles, "6's")
    if "asia" in channel.lower():
        return get_roles('AsiaFortress', roles, "6's")
    if "ozfort" in channel.lower():
        return get_roles('OzFortress', roles, "6's")


def get_roles(region, roles, gamemode):
    for role in roles:
        if region in role.name and gamemode in role.name:
            return parse_role(role.name)


def parse_role(role):
    role = role.split(' ')
    return " ".join(role[2:-1])


def get_skill(role_name):
    skills_nums = {
        'open': 1,
        'low': 2,
        'mid': 3,
        'division 2': 4,
        'division 1': 5,
        'premiership': 6
    }

    return skills_nums[role_name.lower().strip()]