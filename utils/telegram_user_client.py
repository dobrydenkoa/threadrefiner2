# utils/telegram_user_client.py
import os
from telethon.sync import TelegramClient
from telethon.tl.types import Message
import datetime
import json

api_id = int(os.getenv("TELETHON_API_ID"))
api_hash = os.getenv("TELETHON_API_HASH")
session_name = "user_session"

client = TelegramClient(session_name, api_id, api_hash)

async def get_last_24h_messages(chat_id: int) -> str:
    messages = []
    now = datetime.datetime.utcnow()
    yesterday = now - datetime.timedelta(days=1)

    async with client:
        async for msg in client.iter_messages(chat_id, offset_date=now):
            if msg.date < yesterday:
                break
            if isinstance(msg, Message):
                messages.append({
                    "sender_id": msg.sender_id,
                    "text": msg.text,
                    "date": str(msg.date),
                })

    return json.dumps(messages, ensure_ascii=False, indent=2)

