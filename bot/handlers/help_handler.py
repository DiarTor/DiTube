from bot.database import users_collection
from langs import persian, english
from telegram import Update
from telegram.ext import ContextTypes


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if users_collection.find_one({"user_id": user.id})["settings"]["language"] == "fa":
        await update.message.reply_text(f"{persian.guide}")
    elif users_collection.find_one({"user_id": user.id})["settings"]["language"] == "en":
        await update.message.reply_text(f"{english.guide}")


async def adminhelp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not users_collection.find_one({"is_staff": True, "user_id": update.effective_user.id}):
        await update.message.reply_text("❌شما دسترسی به این دستور را ندارید.")
        return
    await update.message.reply_text("/send - Send message to a user\n/sendall - Send message to all users")
