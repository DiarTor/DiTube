from bot.database import users_collection
from langs import persian, english
from telegram import Update
from telegram.ext import ContextTypes


async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if users_collection.find_one({"user_id": user.id})["settings"]["language"] == "fa":
        await update.message.reply_text(persian.donate, parse_mode='markdown', disable_web_page_preview=True)
    elif users_collection.find_one({"user_id": user.id})["settings"]["language"] == "en":
        await update.message.reply_text(english.donate, parse_mode='markdown', disable_web_page_preview=True)
