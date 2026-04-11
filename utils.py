from os.path import join
from os import remove
import discord
from discord import HTTPException
from emoji import emojize

import settings


# Returns a path relative to the bot directory
def get_rel_path(rel_path):
    return join(settings.BASE_DIR, rel_path)


# Returns an emoji as required to send it in a message
# You can pass the emoji name with or without colons
# If fail_silently is True, it will not raise an exception
# if the emoji is not found, it will return the input instead
def get_emoji(emoji_name, fail_silently=False):
    alias = emoji_name if emoji_name[0] == emoji_name[-1] == ":" else f":{emoji_name}:"
    try:
        the_emoji = emojize(alias, language='alias')
    except Exception:
        the_emoji = alias

    if the_emoji == alias and not fail_silently:
        raise ValueError(f"Emoji {alias} not found!")

    return the_emoji


# A shortcut to get a channel by a certain attribute
# Uses the channel name by default
# If many matching channels are found, returns the first one
def get_channel(client, value, attribute="name"):
    # Try to get channel directly first (pycord optimized approach)
    channel = discord.utils.get(client.get_all_channels(), **{attribute: value})
    if channel:
        return channel
    
    # Fallback: iterate through all channels
    for c in client.get_all_channels():
        if getattr(c, attribute, None) and getattr(c, attribute, None).lower() == value.lower():
            return c
    
    raise ValueError("No such channel")


# Shortcut method to send a message in a channel with a certain name
# You can pass more positional arguments to send
# Uses get_channel, so you should be sure that the bot has access to only
# one channel with such name
async def send_in_channel(client, channel_name, *args):
    channel = get_channel(client, channel_name)
    await channel.send(*args)


# Attempts to upload a file in a certain channel
# content refers to the additional text that can be sent alongside the file
# delete_after_send can be set to True to delete the file afterwards
async def try_upload_file(
    client, channel, file_path, content=None, delete_after_send=False, retries=3
):
    import discord
    used_retries = 0
    sent_msg = None

    while not sent_msg and used_retries < retries:
        try:
            with open(file_path, 'rb') as f:
                sent_msg = await channel.send(content=content, file=discord.File(f, file_path.split('/')[-1]))
        except HTTPException:
            used_retries += 1

    if delete_after_send:
        remove(file_path)

    if not sent_msg:
        await channel.send("Oops, something happened. Please try again.")

    return sent_msg

def parse_mention(mention: str):
    """turns a mention into an id string"""
    id = mention.replace(">", "")
    id = id.replace("<@", "")
    return id.split("!")[-1]
