import os
from telethon import TelegramClient, events

# Get from Render Env Vars
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
# For userbot, we use SESSION_STRING, not BOT_TOKEN
session_str = os.getenv("SESSION_STRING") 

# If you use a .session file, use TelegramClient('bot_session', ...)
client = TelegramClient(session_str, api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def view_once_saver(event):
    # Check if message has media with self-destruct timer
    if event.message.media and getattr(event.message.media, 'ttl_seconds', None):
        print(f"View-Once detected from {event.sender_id}, ttl: {event.message.media.ttl_seconds}")
        try:
            # Download the media to memory/file
            path = await event.download_media()
            print(f"Saved to: {path}")

            # Forward to Saved Messages
            await client.send_file(
                'me',
                path,
                caption=f"Saved View-Once from {event.sender_id}\nOriginal Date: {event.message.date}"
            )
            print("Forwarded to Saved Messages")
            # Delete local file after
            if path and os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"Failed to save view-once: {e}")

    # Also save normal media if you want
    # elif event.message.media:
    #    await client.forward_messages('me', event.message)

async def main():
    await client.start()
    print("LiveJack View-Once Saver is running...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
