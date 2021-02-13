from telethon.sync import TelegramClient


api_id = None
api_hash = None


def get_client():
    client = TelegramClient('client', api_id, api_hash)
    return client
