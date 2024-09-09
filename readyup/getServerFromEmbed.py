from getserver import get_server


async def mapMessageHandler(embed, gameID):
    # message = await channel.fetch_message(msgID)
    map = processEmbed(embed)
    ip = get_servemeServer(map)
    connectStr = f"The ip for game {gameID} is: \n {ip}"
    return connectStr


# Processes a specirfic message with an embed in
# This embed should contain a map name, this map name is process and returned
def processEmbed(embed):
    map_embed = embed.fields[-1]
    map_name_bold = map_embed.value
    map_name = map_name_bold.replace("*", "")
    return map_name


# get a server ip from map, currently hard coded for eu
def get_servemeServer(map_name):
    ip, rcon = get_server(map_name, "eu")
    return ip
