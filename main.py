#!venv/bin/python

"""
Forwarder bot v0.1
THIS PRODUCT IS NOT DEBUGGED !
Written by: https://github.com/mehdiirh

1) Create an isolated virtual environment using: `python -m venv venv`
2) Install requirements using: `pip install -r requirements.txt`
3) add your API_ID and API_HASH to ~/Login.py
4) Change data manually from :: ~/plugins/jsons/data.json
5) run this file ( main.py )
6) Enter your credential and login
"""

from Login import get_client
from plugins.utils import Data
from telethon.sync import events
from Types import *
from telethon.tl.types import User
import re
import logging


# ==================
data_manager = Data()
client = get_client()
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
client.start()
print("FORWARDER BOT STARTED ;)")
# ==================


@client.on(events.NewMessage(incoming=True))
async def forwarder(message: Message):
    chat_id = message.chat_id

    if chat_id not in data_manager.channels:
        sender: User = await message.get_sender()
        if sender.username not in data_manager.channels:
            return

    msg: str = message.raw_text

    if not any(word in msg for word in data_manager.words):
        return

    await client.forward_messages(data_manager.group_id, message)


@client.on(events.NewMessage(outgoing=True, pattern=r'.(?:add|remove) ([1-9a-zA-Z][a-zA-Z0-9_]{4,})'))
async def add_remove_channels(message: Message):
    msg: str = message.raw_text
    msg = msg.replace('@', '')
    pattern = re.compile(r'.((?:add|remove)) ([1-9a-zA-Z][a-zA-Z0-9_]{4,})')

    match = pattern.match(msg)
    if not match:
        return

    action = match.group(1).lower()
    channel = match.group(2)

    try:
        channel = await client.get_entity(channel)
    except:
        await message.edit('یوزرنیم وجود ندارد')

    channel_id = str(channel.id)

    if action == 'add':
        data_manager.add_to_file('channels', channel_id)
    elif action == 'remove':
        data_manager.remove_from_file('channels', channel_id)


@client.on(events.NewMessage(outgoing=True, pattern=r'.(?:addword|rmword) (.+)'))
async def add_remove_words(message: Message):
    msg: str = message.raw_text
    pattern = re.compile(r'.((?:addword|rmword)) (.+)')

    match = pattern.match(msg)
    if not match:
        return

    action = match.group(1).lower()
    word = match.group(2)

    if action == 'addword':
        data_manager.add_to_file('words', word)
    elif action == 'rmword':
        data_manager.remove_from_file('words', word)


client.run_until_disconnected()
