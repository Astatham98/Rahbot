from commands.base_command import BaseCommand
from database import Database
import discord
import re


class Warnings(BaseCommand):
    def __init__(self):
        description = ";warnings give @user druation reason, ;warnings get @user"
        params = ["get/give", "player@"]
        self.db = Database()
        super().__init__(description, params)

    async def handle(self, params, message, client):
        command_type = params[0].lower()
        player = params[1]
        player_id = self.parse_mention(player)
        username = self.get_username(player_id, client)

        if command_type == "give":
            await self.warn_player(player_id, message, params, username)
        elif command_type == "get":
            dates, reasons = await self.get_player(player_id, message.channel)
            embed = self.gen_warnings_embed(username, dates, reasons)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("Incorrect parameter input")

    def parse_mention(self, mention: str):
        """turns a mention into an id string"""
        id = mention.replace(">", "")
        id = id.replace("<@!", "")
        return id.replace("<@", "")

    def get_username(self, id, client):
        user = client.get_user(int(id))
        if user is None:
            return
        return user.display_name

    async def get_player(self, player_id, channel):
        warn_list = self.db.get_warned_player(str(player_id))
        if warn_list is not None:
            dates, reasons = [], []
            for warn in warn_list:
                dates.append(warn[1])
                reasons.append(warn[2])
            return dates, reasons
        else:
            await channel.send("User is not in the warnings list")
            return None

    async def warn_player(self, player_id, message, params, player_username):
        # Default duration of 1 day
        duration, readable = (
            self.convert_duration(params[2]) if params[2] is not None else 1440
        )
        reason = params[3] if params[3] is not None else ""
        self.db.warn_player(player_id, duration, reason)

        await message.channel.send(
            f"{player_username} has been logged in the database as warned for {readable}"
        )

    def convert_duration(self, duration):
        conv_dur = 1440
        readable = "24 hours"
        if duration.lower() in ("p", "perma", "permanent"):
            # 5 years
            conv_dur = 526000 * 5
            readable = "5 years"
        else:
            duration = duration.strip()
            splits = re.split("(\d+)", duration)
            duration_time = int(splits[1])
            time_val = splits[2]

            if time_val in ("h", "hour", "hours"):
                conv_dur = duration_time * 60
                readable = f"{duration_time} hour(s)"
            elif time_val in ("d", "day", "days"):
                conv_dur = duration_time * 1440
                readable = f"{duration_time} day(s)"
            elif time_val in ("m", "min", "mins", "minute", "minutes"):
                conv_dur = duration_time * 1
                readable = f"{duration_time} minute(s)"
            elif time_val in ("w", "week", "weeks"):
                conv_dur = duration_time * 1440 * 7
                readable = f"{duration_time} week(s)"
            elif time_val in ("m", "month", "months"):
                conv_dur = duration_time * 43800
                readable = f"{duration_time} months(s)"
            elif time_val in ("s", "sec", "secs", "second", "seconds"):
                conv_dur = duration_time * (1 / 60)
                readable = f"{duration_time} second(s)"

        return conv_dur, readable

    def gen_warnings_embed(self, username, dates, reasons):
        embed = discord.Embed(title=username, colour=discord.Colour.dark_orange())
        text = ""
        for i in range(len(dates)):
            text += f"banneds for {dates[i]} minutes for: {reasons[i]}\n"
        embed.add_field(name="Warnings", value=text, inline=True)
        return embed
