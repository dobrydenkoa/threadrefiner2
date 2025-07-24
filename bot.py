# bot.py
import os
import logging
from telegram import Update, Message
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from utils.mistral_client import ask_mistral
from utils.telegram_user_client import get_last_24h_messages, client

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)

async def handle_forwarded_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message: Message = update.message

    if not message.forward_from_chat:
        await message.reply_text("⚠️ Будь ласка, переслане повідомлення повинно бути з чату.")
        return

    chat_id = message.forward_from_chat.id
    await message.reply_text("📥 Отримано. Збираю історію чату за 24 години...")

    try:
        json_history = await get_last_24h_messages(chat_id)
        await message.reply_text("✅ Історію зібрано. Відправляю в Mistral...")

        reply = ask_mistral(
            f"Проаналізуй історію повідомлень цього чату за 24 години:\n{json_history}"
        )
        await message.reply_text(f"🧠 Відповідь Mistral:\n\n{reply}")

    except Exception as e:
        await message.reply_text(f"❌ Помилка: {e}")

if __name__ == "__main__":
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.FORWARDED & filters.TEXT, handle_forwarded_message))
    print("🤖 Бот запущено!")
    app.run_polling()

