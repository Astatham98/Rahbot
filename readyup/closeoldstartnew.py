async def close(message):
    async for message in message.channel.history(limit=5):
        if message.author.name == 'Raid Organizer':
            await message.delete()
        elif message.author.bot and message.embeds:
            await message.delete(delay=600.0)
        elif message.author.bot:
            await message.delete(delay=30.0)


async def fail_close(message):
    async for message in message.channel.history(limit=5):
        if message.author.name == 'Raid Organizer':
            await message.delete()


async def open(message):
    msg = '!create "pug" 2025-04-05'
    await message.channel.send(msg, delete_after=5.0)


async def close_open(message, ready=False):
    await close(message) if ready else await fail_close(message)
    await open(message)
