from commands.base_command import BaseCommand
import settings
from database import Database
import random
import time


class MedicPicker(BaseCommand):
    def __init__(self):
        description = "Picks a from your most recent game or mention yourself after to gain immunity."
        params = None
        self.db = Database()
        super().__init__(description, params)

    async def handle(self, params, message, client):
        guild = message.guild
        if len(params) > 0:
            id = self.parse_mention(params[0])
            self.db.set_immune(id)

            chosen_player = guild.get_member(int(id))
            await message.channel.send(f'{chosen_player.nick if chosen_player.nick else chosen_player.name} has been given immunity.')
        else:
            team = [x[0] for x in self.db.find_teammates(str(message.author.id))]
            if len(team) > 0:
                chosen_player_id = random.choice(team)
                chosen_player = guild.get_member(int(chosen_player_id))

                users = [guild.get_member(int(chosen_player_id)) for x in team if x is not '']
                await message.channel.send(f'Choosing a medic from: {", ".join([x.nick if x.nick else x.name for x in users])}')

                time.sleep(0.5)
                await message.channel.send(f"{chosen_player.nick if chosen_player.nick else chosen_player.name} has been selected to play medic.")
                self.db.set_immune(chosen_player_id)
            else:
                await message.channel.send('Unable to find the corresponding team.')
       
    def find_team(self, message):
        author = message.author
        teams = [x for x in settings.CURRENT_GAME.values()]
        if len(teams) > 0:
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
        id = id.replace('<@!', '')
        return id.replace('<@', '')
        
