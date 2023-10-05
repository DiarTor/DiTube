from bot.database import users_collection
from bot.download_videos.get_video_information import get_video_options
from bot.users.settings.language import join_in_selecting_lang
from bot.users.settings.language import selected_lang_is_en, selected_lang_is_fa
from bot.users.settings.settings import join_in_settings
from langs import persian, english
from pytube import YouTube
from pytube.exceptions import AgeRestrictedError
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import ContextTypes
from utils.buttons import homepage_buttons
from utils.check_user_settings import check_user_lang
from utils.is_channel_sub import check_sub


async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    support_channel_id = -925489226
    chat_id = update.effective_chat.id
    user_message = update.message
    user_message_text = update.message.text
    user_reply = update.message.reply_to_message
    user_photo = update.message.photo
    user = update.effective_user
    if not await check_sub(update, context, user.id):
        await update.message.reply_text(f"Please subscribe and then use /start.\n @diardev")
        return
    elif not users_collection.find_one({"user_id": user.id}):
        await update.message.reply_text(f"{persian.restart}\n\n{english.restart}")
        return
    elif user_message_text.startswith("https://youtu.be/"):
        user_lang = users_collection.find_one({"user_id": user.id})["settings"]["language"]
        geting_info_response = persian.get_video_info if user_lang == "fa" else english.get_video_info
        message_info = await update.message.reply_text(geting_info_response, quote=True)
        kb = []
        yt = YouTube(user_message_text)
        try:
            video_options = get_video_options(yt)
        except AgeRestrictedError:
            response = persian.age_restricted if user_lang == "fa" else english.age_restricted
            await update.message.reply_text(response, quote=True)
            return
        for item in sorted(video_options, reverse=True):
            parts = item.split()
            if len(parts) == 2:
                quality, size = parts
                kb.append([InlineKeyboardButton(f"{quality} {size}",
                                                callback_data=f"{user_message_text} {quality} {chat_id}")])
        if user_lang == "en":
            kb.append([InlineKeyboardButton(f"Download Audio", callback_data=f"{user_message_text} vc {chat_id}")])
        else:
            kb.append([InlineKeyboardButton(f"دانلود صوت", callback_data=f"{user_message_text} vc {chat_id}")])
        reply_markup = InlineKeyboardMarkup(kb)
        response = persian.select_quality if user_lang == "fa" else english.select_quality
        await update.message.reply_text(response, reply_markup=reply_markup, quote=True)
        await message_info.delete()
    elif user_message_text.startswith("https://youtube.com/shorts/"):
        user_lang = users_collection.find_one({"user_id": user.id})["settings"]["language"]
        geting_info_response = persian.get_video_info if user_lang == "fa" else english.get_video_info
        message_info = await update.message.reply_text(geting_info_response, quote=True)
        kb = []
        yt = YouTube(user_message_text)
        try:
            video_options = get_video_options(yt)
        except AgeRestrictedError:
            response = persian.age_restricted if user_lang == "fa" else english.age_restricted
            await update.message.reply_text(response, quote=True)
            return
        for item in sorted(video_options, reverse=True):
            parts = item.split()
            if len(parts) == 2:
                quality, size = parts
                kb.append([InlineKeyboardButton(f"{quality} {size}",
                                                callback_data=f"{user_message_text} {quality} {chat_id}")])
        reply_markup = InlineKeyboardMarkup(kb)
        response = persian.select_quality if user_lang == "fa" else english.select_quality
        await update.message.reply_text(response, reply_markup=reply_markup, quote=True)
        await message_info.delete()
    elif user_message_text == "Return" or user_message_text == "بازگشت":
        user_lang = check_user_lang(user_id=user.id)
        response = "Returned to the main menu" if user_lang == "en" else "بازگشت به صفحه اصلی"
        await update.message.reply_text(response, reply_markup=ReplyKeyboardMarkup(homepage_buttons(user.id),
                                                                                   resize_keyboard=True))
        if context.user_data.get("joined_in_settings") or context.user_data.get("selecting_lang"):
            context.user_data["joined_in_settings"] = False
            context.user_data["selecting_lang"] = False
    elif user_message_text == "⚙️ تنظیمات" or user_message_text == "⚙️ Settings":
        await join_in_settings(update, context)
    elif context.user_data.get("joined_in_settings"):
        if user_message_text == "Change Language" or user_message_text == "تغییر زبان":
            await join_in_selecting_lang(update, context)
            context.user_data["joined_in_settings"] = False
        else:
            user_lang = check_user_lang(user_id=user.id)
            response = persian.didnt_understand if user_lang == "fa" else english.didnt_understand
            await update.message.reply_text(response, quote=True)
    elif context.user_data.get('selecting_lang'):
        if user_message_text == "🇮🇷فارسی":
            await selected_lang_is_fa(update, context)
        elif user_message_text == "🇺🇸English":
            await selected_lang_is_en(update, context)
        else:
            await update.message.reply_text(
                f"ببخشید ولی منظورتان را متوجه نشدم🧐 لطفا از دکمه های زیر استفاده کنید👇\nSorry i didn't get what you mean, please select the buttons below.")
    elif check_user_lang(user_id=user.id) == "not_selected":
        context.user_data['selecting_lang'] = True
        await update.message.reply_text(f"{persian.restart}\n\n{english.restart}")
    else:
        user_lang = check_user_lang(user_id=user.id)
        response = persian.didnt_understand if user_lang == "fa" else english.didnt_understand
        await update.message.reply_text(response, quote=True)
