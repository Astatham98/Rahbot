import sys
import settings
import discord
from discord import ApplicationContext, slash_command, option
import message_handler
from organiserBotHandle import OrganiserBotHandle
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from events.base_event import BaseEvent
from events import *
import slash_commands

# Set to remember if the bot is already running, since on_ready may be called
# more than once on reconnects
this = sys.modules[__name__]
this.running = False

# Scheduler that will be used to manage events
sched = AsyncIOScheduler()

# Intents setup
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True
intents.messages = True


###############################################################################


def main():
    # Initialize the bot with slash command support
    print("Starting up...")
    client = discord.Bot(intents=intents, command_prefix=settings.COMMAND_PREFIX)
    
    @client.slash_command(name="help", description="Displays help message with all available commands")
    async def slash_help_handler(ctx: discord.ApplicationContext):
        await slash_commands.help_slash(ctx)
    # Register slash commands
    @client.slash_command(name="leaderboard", description="Show the games played leaderboard")
    @option("page", description="Initial page number (default: 1)", required=False)
    @option("player", description="Player to check leaderboard position for", required=False)
    async def slash_leaderboard(ctx: discord.ApplicationContext, page: int = 1, player: discord.Member = None):
        await slash_commands.leaderboard_slash(ctx, page, player)
        
    @client.slash_command(name="rank", description="Show player rank information")
    @option("player", description="Player to check rank for (default: yourself)", required=False)
    async def slash_rank(ctx: discord.ApplicationContext, player: discord.Member = None):
        await slash_commands.rank_slash(ctx, player)
        
    @client.slash_command(name="warnings", description="Manage player warnings")
    @option("mode", description="Mode: get or give", required=True, choices=["get", "give"])
    @option("player", description="Player to warn or view warnings for", required=False)
    @option("duration", description="Warning duration (e.g. 1h, 3d, 1w, permanent)", required=False)
    @option("reason", description="Reason for the warning", required=False)
    async def slash_warnings(ctx: discord.ApplicationContext, mode: str, player: discord.Member = None, duration: str = None, reason: str = None):
        await slash_commands.warnings_slash(ctx, mode, player, duration, reason)
        
    @client.slash_command(name="setup", description="Setup roles or database tables")
    @option("target", description="roles or db", required=False, choices=["roles", "db"])
    @option("update", description="For roles: update missing roles / colors", required=False)
    async def slash_setup(ctx: discord.ApplicationContext, target: str = "roles", update: bool = False):
        await slash_commands.setup_slash(ctx, target, update)
        
    @client.slash_command(name="getdiv", description="Get division role based on your player profile")
    @option("profile_url", description="Your player profile URL", required=True)
    async def slash_getdiv(ctx: discord.ApplicationContext, profile_url: str):
        await slash_commands.getdiv_slash(ctx, profile_url)
        
    @client.slash_command(name="medicpicker", description="Pick a medic from your last game or set immunity")
    @option("player", description="Player to grant immunity (admin only)", required=False)
    async def slash_medicpicker(ctx: discord.ApplicationContext, player: discord.Member = None):
        await slash_commands.medicpicker_slash(ctx, player)
        
    @client.slash_command(name="getserver", description="Get a reserved server for your game")
    @option("map_choice", description="Map shortname (e.g. process, sunshine, product)", required=True)
    @option("location", description="Optional location override: de/fr/nl/", required=False, choices=["de", "fr", "nl"])
    async def slash_getserver(ctx: discord.ApplicationContext, map_choice: str, location: str = None):
        await slash_commands.getserver_slash(ctx, map_choice, location)

    @client.slash_command(name="getuseraccounts", description="Get user account links by mention/profile/id")
    @option("query", description="@user, etf2l profile, or steam profile/id", required=True)
    async def slash_getuseraccounts(ctx: discord.ApplicationContext, query: str):
        await slash_commands.getuseraccounts_slash(ctx, query)

    @client.slash_command(name="mentionmode", description="Get or set mention mode (admin only)")
    @option("mode", description="Optional mode value: 0 or 1", required=False, choices=[0, 1])
    async def slash_mentionmode(ctx: discord.ApplicationContext, mode: int = None):
        await slash_commands.mentionmode_slash(ctx, mode)

    @client.slash_command(name="editrolecolor", description="Edit role color (admin only)")
    @option("role_name", description="Role name to edit", required=True)
    @option("color", description="Hex or color name", required=True)
    async def slash_editrolecolor(ctx: discord.ApplicationContext, role_name: str, color: str):
        await slash_commands.editrolecolor_slash(ctx, role_name, color)

    @client.slash_command(name="editrolename", description="Rename a role or mass update rank suffix (admin only)")
    @option("new_name", description="New role name or suffix", required=True)
    @option("role_name", description="Role to rename (ignored for mass mode)", required=False)
    @option("mass", description="Set true to mass-update division roles", required=False)
    async def slash_editrolename(
        ctx: discord.ApplicationContext,
        new_name: str,
        role_name: str = None,
        mass: bool = False,
    ):
        await slash_commands.editrolename_slash(ctx, role_name, new_name, mass)

    @client.slash_command(name="rundb", description="DB maintenance operations (admin only)")
    @option("action", description="reset, set_played, or remove", required=True, choices=["reset", "set_played", "remove"])
    @option("player", description="Player to modify", required=True)
    @option("amount", description="Amount for set_played/remove", required=False)
    async def slash_rundb(
        ctx: discord.ApplicationContext,
        action: str,
        player: discord.Member,
        amount: int = None,
    ):
        await slash_commands.rundb_slash(ctx, action, player, amount)
        
    

    # Define event handlers for the client
    # on_ready may be called multiple times in the event of a reconnect,
    # hence the running flag
    @client.event
    async def on_ready():
        if this.running:
            return

        this.running = True

        # Set the playing status
        if settings.NOW_PLAYING:
            print("Setting NP game", flush=True)
            await client.change_presence(
                activity=discord.Game(name=settings.NOW_PLAYING)
            )
        print("Logged in!", flush=True)

        # Load all events
        print("Loading events...", flush=True)
        n_ev = 0
        for ev in BaseEvent.__subclasses__():
            event = ev()
            sched.add_job(
                event.run, "interval", (client,), minutes=event.interval_minutes
            )
            n_ev += 1
        sched.start()
        print(f"{n_ev} events loaded", flush=True)

    # The message handler for both new message and edits
    async def common_handle_message(message):
        text = message.content
        if text.startswith(settings.COMMAND_PREFIX) and text != settings.COMMAND_PREFIX:
            cmd_split = text[len(settings.COMMAND_PREFIX) :].split()
            print(cmd_split)
            try:
                await message_handler.handle_command(
                    cmd_split[0].lower(), cmd_split[1:], message, client
                )
            except:
                print("Error while handling message", flush=True)
                raise

    # Only takes in the message if it is in the desired channels
    @client.listen()
    async def on_message(message: discord.Message):
        if (
            message.channel.type != discord.ChannelType.private
            and message.channel.name in settings.CHANNEL
        ):
            await common_handle_message(message)
        elif (
            message.author.bot
            and len(message.embeds) > 0
            and settings.TRACK in message.channel.name
        ):
            organhandle = OrganiserBotHandle(message.embeds[-1], message, client)
            await organhandle.handle()

    @client.event
    async def on_message_edit(before, after):
        await common_handle_message(after)

    # Finally, set the bot running
    client.run(settings.BOT_TOKEN)


###############################################################################


if __name__ == "__main__":
    main()
