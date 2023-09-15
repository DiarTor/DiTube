from bot.database import users_collection
from langs import english
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram import Update
from telegram.ext import ContextTypes


async def join_send_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not users_collection.find_one({"is_staff": True, "user_id": update.effective_user.id}):
        await update.message.reply_text(english.no_access)
        return
    cancel_button = [[KeyboardButton("Cancel ⬅️")]]
    cancel_reply_markup = ReplyKeyboardMarkup(cancel_button, resize_keyboard=True)
    if context.args and context.args[0].isdigit():
        user_id = int(context.args[0])
        if not users_collection.find_one({"user_id": user_id}):
            await update.message.reply_text(english.user_not_found)
            return
        context.user_data["sending_to_user"] = True
        context.user_data["user_id"] = user_id
        await update.message.reply_text(english.please_send_message, reply_markup=cancel_reply_markup)
    else:
        await update.message.reply_text(english.send_user_id_usage)


async def send_msg_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text:
        message = update.message.text
        user_id = context.user_data.get("user_id")
        if user_id is not None:
            await context.bot.send_message(chat_id=user_id, text=message)
            await update.message.reply_text(english.message_sent_to_user, reply_markup=ReplyKeyboardRemove())
            context.user_data["sending_to_user"] = False
            context.user_data["user_id"] = None
        else:
            await update.message.reply_text(english.user_not_specified)
    elif update.message.photo:
        photo = update.message.photo[-1].file_id
        if update.message.caption:
            caption = update.message.caption
        else:
            caption = None
        user_id = context.user_data.get("user_id")
        if user_id is not None:
            await context.bot.send_photo(chat_id=user_id, photo=photo, caption=caption)
            await update.message.reply_text(english.image_sent_to_user, reply_markup=ReplyKeyboardRemove())
            context.user_data["sending_to_user"] = False
            context.user_data["user_id"] = None
        else:
            await update.message.reply_text(english.user_not_specified)


async def join_sending_to_all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not users_collection.find_one({"is_staff": True, "user_id": update.effective_user.id}):
        await update.message.reply_text(english.no_access)
        return
    cancel_button = [[KeyboardButton("Cancel ⬅️")]]
    cancel_reply_markup = ReplyKeyboardMarkup(cancel_button, resize_keyboard=True)
    context.user_data["sending_to_all"] = True
    await update.message.reply_text(english.please_send_message, reply_markup=cancel_reply_markup)


async def send_msg_to_all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    documents = users_collection.find()
    for doc in documents:
        chat_id = doc['user_id']
    if update.message.text:
        message = update.message.text
        await context.bot.send_message(chat_id=chat_id, text=message, reply_markup=ReplyKeyboardRemove())
        await update.message.reply_text(english.message_sent_to_all)
        context.user_data["sending_to_all"] = False
    elif update.message.photo:
        photo = update.message.photo[-1].file_id
        if update.message.caption:
            caption = update.message.caption
        else:
            caption = ""
        await context.bot.send_photo(chat_id=chat_id, photo=photo, caption=caption, reply_markup=ReplyKeyboardRemove())
        await update.message.reply_text(english.image_sent_to_all)
        context.user_data["sending_to_all"] = False
