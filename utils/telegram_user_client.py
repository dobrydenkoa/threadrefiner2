from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel
from telethon.tl.functions.messages import GetHistoryRequest
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_NAME = "anon"  # або можеш назвати по-своєму

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def fetch_chat_history(chat_id: int, from_date: datetime, to_date: datetime):
    await client.start()
    history = []

    offset_id = 0
    limit = 100

    while True:
        messages = await client(GetHistoryRequest(
            peer=PeerChannel(chat_id),
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))

        if not messages.messages:
            break

        for msg in messages.messages:
            msg_date = msg.date.replace(tzinfo=None)
            if from_date <= msg_date <= to_date:
                history.append({
                    "date": msg.date.isoformat(),
                    "sender_id": msg.from_id.user_id if msg.from_id else None,
                    "text": msg.message
                })

        offset_id = messages.messages[-1].id

        if messages.messages[-1].date.replace(tzinfo=None) < from_date:
            break

    return history
