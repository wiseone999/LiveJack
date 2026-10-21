import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_str = os.environ.get("SESSION_STRING")

client = TelegramClient(StringSession(session_str), api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    if event.message.media:
        ttl = getattr(event.message.media, 'ttl_seconds', None)
        if ttl:
            print("View-once detected, saving...")
            await client.send_file('me', event.message.media, caption="View-Once Saved")

print("LiveJack Running...")
client.start()
client.run_until_disconnected()
