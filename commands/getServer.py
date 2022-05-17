from commands.base_command import BaseCommand
from getserver import get_server


class Getserver(BaseCommand):
    def __init__(self):
        description = "Gets a french server with whatever map you want."
        params = ["map"]
        super().__init__(description, params)

    async def handle(self, params, message, client):
        map_choice = params[0]
        server_loc = message.channel.name.split('-')[0]
        if len(params) > 1: 
            if params[1].lower() in ("de", "fr", "nl"): 
                server_loc += " " + params[1]
            elif params[1].lower() in ("chi", "ks", "la"):
                server_loc += " " + params[1]
        server, rcon = get_server(map_choice, server_loc)
        if server is None: 
            if rcon is None:
                await message.channel.send('Please enter a valid map name')
            else:
                await message.channel.send('ERROR ACCESSING THE API')
        else:
            await message.channel.send('Server IP is: \n{}'.format(server))
        
            dm_channel = await message.author.create_dm()
            await dm_channel.send("The rcon string for this server is:\nrcon_address {}; rcon_password {}".format(server.split(" ")[1].replace(";",""), rcon))
