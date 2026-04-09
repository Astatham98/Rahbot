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
    @option("page", description="Page number to display (default: 1)", required=False)
    async def slash_leaderboard(ctx: discord.ApplicationContext, page: int = 1):
        await slash_commands.leaderboard_slash(ctx, page)
        
    @client.slash_command(name="rank", description="Show player rank information")
    @option("player", description="Player to check rank for (default: yourself)", required=False)
    async def slash_rank(ctx: discord.ApplicationContext, player: discord.Member = None):
        await slash_commands.rank_slash(ctx, player)
        
    @client.slash_command(name="warnings", description="Manage player warnings")
    @option("player", description="Player to warn or view warnings for", required=False)
    @option("duration", description="Warning duration (e.g. 1h, 3d, 1w, permanent)", required=False)
    @option("reason", description="Reason for the warning", required=False)
    async def slash_warnings(ctx: discord.ApplicationContext, player: discord.Member = None, duration: str = None, reason: str = None):
        await slash_commands.warnings_slash(ctx, player, duration, reason)
        
    @client.slash_command(name="setup", description="Setup bot database tables")
    async def slash_setup(ctx: discord.ApplicationContext):
        await slash_commands.setup_slash(ctx)
        
    @client.slash_command(name="getdiv", description="Get division role based on your player profile")
    @option("profile_url", description="Your player profile URL", required=True)
    async def slash_getdiv(ctx: discord.ApplicationContext, profile_url: str):
        await slash_commands.getdiv_slash(ctx, profile_url)
        
    @client.slash_command(name="medicpicker", description="Pick a medic from your last game or set immunity")
    @option("player", description="Player to grant immunity (admin only)", required=False)
    async def slash_medicpicker(ctx: discord.ApplicationContext, player: discord.Member = None):
        await slash_commands.medicpicker_slash(ctx, player)
        
    @client.slash_command(name="getserver", description="Get a reserved server for your game")
    async def slash_getserver(ctx: discord.ApplicationContext):
        await slash_commands.getserver_slash(ctx)
        
    

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
