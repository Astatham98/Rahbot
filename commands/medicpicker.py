from commands.base_command import BaseCommand
import settings
from database import Database
import random


class MedicPicker(BaseCommand):
    def __init__(self):
        description = "Picks a medic"
        params = None
        self.db = Database()
        super().__init__(description, params)

    async def handle(self, params, message, client):
        if len(params) > 0:
            id = self.parse_mention(params[0])
            self.db.set_immune(id)

            chosen_player = await client.fetch_user(int(id))
            await message.channel.send(f'{chosen_player.name} has been given immunity.')
        else:
            team = self.find_team(message)
            if team is not None:
                eligible = []
                for player in team:
                    if self.db.immune(player) is False:
                        eligible.append(player)
                
                chosen_player_id = random.choice(eligible)
                chosen_player = await client.fetch_user(int(chosen_player_id))
                
                await message.channel.send(f"{chosen_player.name} has been selected to play medic.")
                self.db.set_immune(chosen_player_id)
            else:
                await message.channel.send('Unable to find the corresponding team.')
       
    def find_team(self, message):
        author = message.author
        teams = [x for x in settings.CURRENT_GAME.values()]
        red, blue = teams[0], teams[1]
        print(red, blue)

        if str(author.id) in red:
            return red
        elif str(author.id) in blue:
            return blue
        return None

    def parse_mention(self, mention: str):
        """turns a mention into an id string"""
        id = mention.replace('>', '')
        id = id.replace('<@', '')
        return id
