from telegram import Update
from telegram.ext import ContextTypes

from bot.database import users_collection
from langs import persian, english


async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if users_collection.find_one({"user_id": user.id})['lang'] == "fa":
        await update.message.reply_text(persian.donate, parse_mode='markdown')
    elif users_collection.find_one({"user_id": user.id})['lang'] == "en":
        await update.message.reply_text(english.donate, parse_mode='markdown')
