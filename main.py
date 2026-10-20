import os
from telethon import TelegramClient, events

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

client = TelegramClient("view_once_saver", API_ID, API_HASH)

@client.on(events.NewMessage)
async def handler(event):
    msg = event.message
    if msg.media and getattr(msg.media, 'ttl_seconds', None):
        print("View Once found, saving...")
        path = await msg.download_media(file="saved_media/")
        print(f"Saved to: {path}")

print("Bot running...")
client.start()
client.run_until_disconnected()
