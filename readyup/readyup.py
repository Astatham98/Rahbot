import discord
import utils
import asyncio
import copy
from readyup import closeoldstartnew


class Ready:
    def __init__(self, members_list, message, client):
        self.members_list = copy.copy(members_list)
        self.message = message
        self.client = client
        self.timeout = False

    async def ready_up(self):
        msg = await self.create_message()
        while self.members_list and not self.timeout:
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=90.0, check=self.check)
                correct_emoji = await self.remove_reaction(msg, user, reaction)
                if correct_emoji:
                    self.members_list.remove(user)
                    await self.remove_player_from_embed(msg)

            except asyncio.TimeoutError:
                self.timeout = True
                await self.message.channel.send(', '.join([x.name for x in self.members_list]) +
                                                ' did not ready up. Starting a new pug.',
                                                delete_after=20.0)
                await msg.delete()
                await closeoldstartnew.close_open(self.message, False)

        await msg.delete(delay=30.0)
        return not self.timeout

    async def create_message(self):
        val2 = 'Ready up! ' + ' '.join([x.mention for x in self.members_list])

        bot_message = await self.message.channel.send(content=val2, embed=self.create_embed())
        await bot_message.add_reaction(utils.get_emoji("white_check_mark"))

        return bot_message

    def create_embed(self):
        val = '\n'.join([x.name for x in self.members_list]) if self.members_list else "Game Ready!"
        embed = discord.Embed(title="", color=0x11ff00)
        embed.add_field(name="Players", value=val, inline=False)
        return embed

    async def remove_reaction(self, msg, user, emoji):
        # Removes reactions from the message, if desired emoji return the true
        await msg.remove_reaction(emoji, user)

        if str(emoji) != str(utils.get_emoji("white_check_mark")):
            return False
        return True

    def check(self, reaction, user):
        return not user.bot and user.name in [x.name for x in self.members_list]

    async def remove_player_from_embed(self, msg):
        # Removes a user's name from the embed
        await msg.edit(embed=self.create_embed())
