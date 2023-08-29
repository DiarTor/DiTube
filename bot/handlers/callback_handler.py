from telegram import Update
from telegram.ext import CallbackContext

from bot.download.process_video import process


async def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    link, res_code, chat_id = data.split(" ", 2)
    await query.edit_message_text("✨Downloading...")
    await process(update=update, link=link, quality=res_code, chat_id=chat_id)
    await query.delete_message()
