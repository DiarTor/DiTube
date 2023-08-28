from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from bot.database import users_collection


async def send(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not users_collection.find_one({"is_staff": True, "user_id": update.effective_user.id}):
        await update.message.reply_text("❌شما دسترسی به این دستور را ندارید.")
        return
    try:
        if context.args and context.args[0].isdigit() and context.args[1:]:
            user_id = int(context.args[0])
            message = " ".join(context.args[1:])
            await context.bot.send_message(user_id, f"👤یک پیام از مدیریت :\n\n{message}")
            await update.message.reply_text("✅پیام شما ارسال شد.")
        else:
            await update.message.reply_text("Usage: /send <user_id> <message>")
    except BadRequest:
        await update.message.reply_text("❌کاربر یافت نشد!")


async def sendall(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not users_collection.find_one({"is_staff": True, "user_id": update.effective_user.id}):
        await update.message.reply_text("❌شما دسترسی به این دستور را ندارید.")
        return
    if context.args and context.args[0:]:
        documents = users_collection.find()
        message = " ".join(context.args[0:])
        for doc in documents:
            chat_id = doc['user_id']
            await context.bot.send_message(chat_id=chat_id, text=message)
        await update.message.reply_text("✅پیام شما ارسال شد.")
    else:
        await update.message.reply_text("Usage: /sendall <message>")
