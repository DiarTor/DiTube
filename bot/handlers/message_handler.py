from pytube import YouTube
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import ContextTypes

from bot.database import users_collection
from bot.download.get_resolution import get_resolution_options
from bot.handlers.lang_handler import selected_lang_is_en, selected_lang_is_fa
from langs import persian, english


async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    support_channel_id = -925489226
    chat_id = update.effective_chat.id
    user_message = update.message
    user_message_text = update.message.text
    user_reply = update.message.reply_to_message
    user_photo = update.message.photo
    user = update.effective_user
    if not users_collection.find_one({"user_id": user.id}):
        await update.message.reply_text(f"{persian.restart}\n\n{english.restart}")
        return
    elif user_message_text.startswith("https://youtu.be/"):
        kb = []
        yt = YouTube(user_message_text)
        resolution_options = get_resolution_options(yt)
        for res in sorted(resolution_options):
            kb.append([InlineKeyboardButton(
                f"{res}", callback_data=f"{user_message_text} {res} {chat_id}"
            )])
        reply_markup = InlineKeyboardMarkup(kb)
        await update.message.reply_text("❓Choose The Quality :", reply_markup=reply_markup, quote=True)
    elif context.user_data.get('selecting_lang'):
        if user_message_text == "🇮🇷فارسی":
            await selected_lang_is_fa(update, context)
        elif user_message_text == "🇺🇸English":
            await selected_lang_is_en(update, context)
        else:
            await update.message.reply_text(
                f"ببخشید ولی منظورتان را متوجه نشدم🧐 لطفا از دکمه های زیر استفاده کنید👇\nSorry i didn't get what you mean, please select the buttons below.")
    elif users_collection.find_one({"user_id": user.id})["lang"] == "not_selected":
        context.user_data['selecting_lang'] = True
        await update.message.reply_text(f"{persian.restart}\n\n{english.restart}")
    else:
        user_lang = users_collection.find_one({"user_id": user.id})["lang"]
        response = persian.didnt_understand if user_lang == "fa" else english.didnt_understand
        await update.message.reply_text(response)
