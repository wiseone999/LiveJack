import os
import asyncio
from telethon import TelegramClient, events

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

async def main():
    client = TelegramClient("view_once_saver", API_ID, API_HASH)
    await client.start()
    print("Bot running... Saved Messages ready")

    @client.on(events.NewMessage(incoming=True))
    async def handler(event):
        msg = event.message

        # Check View Once
        is_view_once = False
        if msg.media:
            if getattr(msg.media, 'ttl_seconds', None):
                is_view_once = True
            # For photo/video document
            doc = getattr(msg.media, 'document', None)
            if doc and getattr(doc, 'ttl_seconds', None):
                is_view_once = True
            photo = getattr(msg.media, 'photo', None)
            if photo and getattr(photo, 'ttl_seconds', None):
                is_view_once = True
        if getattr(msg, 'ttl_seconds', None):
            is_view_once = True

        if is_view_once:
            print("View Once detected - Saving...")
            try:
                # 1. Download
                path = await event.download_media(file="saved_media/")
                print(f"Downloaded: {path}")

                # 2. Forward to Saved Messages (me)
                if path:
                    await client.send_file(
                        "me",
                        path,
                        caption=f"✅ Saved View Once\nFrom: {event.sender_id}\nID: {msg.id}"
                    )
                    print("✅ Forwarded to Saved Messages")
            except Exception as e:
                print(f"Failed to save: {e}")

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
