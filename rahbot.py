import sys
import settings
import discord
import message_handler
from organiserBotHandle import OrganiserBotHandle
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from events.base_event import BaseEvent
from events import *
from multiprocessing import Process

# Set to remember if the bot is already running, since on_ready may be called
# more than once on reconnects
this = sys.modules[__name__]
this.running = False

# Scheduler that will be used to manage events
sched = AsyncIOScheduler()

# Intents setup
intents = discord.Intents.default()
intents.members = True

###############################################################################

def main():
    # Initialize the client
    print("Starting up...")
    client = discord.Client(intents=intents)

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
                activity=discord.Game(name=settings.NOW_PLAYING))
        print("Logged in!", flush=True)

        # Load all events
        print("Loading events...", flush=True)
        n_ev = 0
        for ev in BaseEvent.__subclasses__():
            event = ev()
            sched.add_job(event.run, 'interval', (client,),
                          minutes=event.interval_minutes)
            n_ev += 1
        sched.start()
        print(f"{n_ev} events loaded", flush=True)

    # The message handler for both new message and edits
    async def common_handle_message(message):
        text = message.content
        if text.startswith(settings.COMMAND_PREFIX) and text != settings.COMMAND_PREFIX:
            cmd_split = text[len(settings.COMMAND_PREFIX):].split()
            try:
                await message_handler.handle_command(cmd_split[0].lower(),
                                                     cmd_split[1:], message, client)
            except:
                print("Error while handling message", flush=True)
                raise

    # Only takes in the message if it is in the desired channels
    @client.event
    async def on_message(message):
        if message.channel.type != discord.ChannelType.private and message.channel.name in settings.CHANNEL:
            await common_handle_message(message)
        elif message.author.bot and len(message.embeds) > 0:
            organhandle = OrganiserBotHandle(message.embeds[-1], message, client)
            await organhandle.handle()

    @client.event
    async def on_message_edit(before, after):
        if len(after.embeds) > 0 and settings.TRACK in after.channel.name:
            organhandle = OrganiserBotHandle(after.embeds[-1], after, client)
            await organhandle.handle()
        else:
            await common_handle_message(after)

    # Finally, set the bot running
    client.run(settings.BOT_TOKEN)


###############################################################################


if __name__ == "__main__":
    main()