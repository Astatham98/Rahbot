from commands.base_command import BaseCommand
from database import Database


class setupDB(BaseCommand):
    def __init__(self):
        description = "Sets up the required databases for a server"
        params = []
        self.db = Database()
        super().__init__(description, params)

    async def handle(self, params, message, client):
        self.setup_leaderboard()
        self.setup_games()
        self.setup_users()
        self.db.close()

    def setup_leaderboard(self):
        self.db.create_leaderboard_table()

    def setup_games(self):
        self.db.create_games_table()

    def setup_users(self):
        self.db.create_users_table()
