from telegram import Update
from telegram.ext import ContextTypes

from bot.database import users_collection
from bot.handlers.lang_handler import join_in_selecting_lang
from langs import persian, english


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_data = {"user_id": user.id, "lang": "not_selected", "is_staff": False, "donated": 0}
    if not users_collection.find_one({"user_id": user.id}):
        users_collection.insert_one(user_data)
    elif users_collection.find_one({"user_id": user.id})["lang"] == "not_selected":
        await join_in_selecting_lang(update, context)
    elif users_collection.find_one({"user_id": user.id})["lang"] == "en":
        await update.message.reply_text(f"{english.greeting}")
    elif users_collection.find_one({"user_id": user.id})["lang"] == "fa":
        await update.message.reply_text(f"{persian.greeting}")
