from commands.base_command import BaseCommand
from database import Database
import discord
import settings


class RunDB(BaseCommand):
    def __init__(self):
        self.db = Database()
        description = "Runs db commands (WIP)"
        params = None
        super().__init__(description, params)

    async def handle(self, params, message, client):
        if message.author.guild_permissions.administrator:
            db = self.db
            db.insert_into_leaderboard(message.author)
        else:
            await message.channel.send('Insufficient rank.')
