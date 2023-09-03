from telegram import Update
from telegram.ext import CallbackContext

from bot.database import users_collection
from bot.download_videos.process_video import process


async def handle_callback(update: Update, context: CallbackContext):
    user_lang = users_collection.find_one({"user_id": update.effective_user.id})["lang"]
    query = update.callback_query
    data = query.data
    link, res_code, chat_id = data.split(" ", 2)
    if not link.startswith("https://youtu.be/"):
        link = f"https://youtube.com/shorts/{link}"
    if user_lang == "en":
        await query.edit_message_text("✨Processing...")
    else:
        await query.edit_message_text("✨درحال پردازش...")
    await process(update=update, link=link, quality=res_code, chat_id=chat_id)
    await query.delete_message()
