from commands.base_command import BaseCommand
from database import Database


class Warnings(BaseCommand):
    def __init__(self):
        description = "Gets or gives warnings"
        params = ["get/give", "player@"]
        self.db = Database()
        super().__init__(description, params)

    async def handle(self, params, message, client):
        pass

    def parse_mention(self, mention: str):
        """turns a mention into an id string"""
        id = mention.replace(">", "")
        id = id.replace("<@!", "")
        return id.replace("<@", "")
