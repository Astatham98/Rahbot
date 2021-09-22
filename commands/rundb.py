from commands.base_command import BaseCommand
from database import Database
import discord
import settings


class RunDB(BaseCommand):
    def __init__(self):
        self.db = Database()
        description = "commands - {reset, player}: sets played to 0, {set_played, player, amount}:" \
                      " sets the amount of games played, {remove, player, amount}: Removes an amount from a player "
        params = ["command"]
        super().__init__(description, params)
        self.commands = ["reset", "set_played", "remove"]

    async def handle(self, params, message, client):
        if not message.author.guild_permissions.administrator:
            await message.channel.send('Insufficient rank.')
        else:
            command = [x for x in self.commands if params[0].lower() == x]
            command = command[0] if command else None

            if not command:
                await message.channel.send('Incorrect input')
            else:
                if command == "reset":
                    self.db.modify_player(params[1], 0)
                elif command == "set_played":
                    self.db.modify_player(params[1], params[2])
                else:
                    self.db.modify_player(params[1], params[2], True)
