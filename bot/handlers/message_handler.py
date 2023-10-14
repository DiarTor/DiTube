import re

from bot.database import users_collection
from bot.handlers.yt_link_handler import youtube_video_handler, youtube_shorts_handler
from bot.users.settings.language import join_in_selecting_lang
from bot.users.settings.language import selected_lang_is_en, selected_lang_is_fa
from bot.users.settings.settings import join_in_settings
from langs import persian, english
from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import ContextTypes
from utils.buttons import homepage_buttons
from utils.get_user_data import get_user_lang, format_subscription_data, get_user_subscription_data
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
    elif re.search(r'https://youtu.be/|https://www.youtube.com/watch\?v=', user_message_text):
        await youtube_video_handler(update, context)
    elif re.search(r"https://youtube.com/shorts/", user_message_text):
        await youtube_shorts_handler(update, context)
    elif user_message_text == "Return" or user_message_text == "بازگشت":
        user_lang = get_user_lang(user_id=user.id)
        response = "Returned to the main menu" if user_lang == "en" else "بازگشت به صفحه اصلی"
        await update.message.reply_text(response, reply_markup=ReplyKeyboardMarkup(homepage_buttons(user.id),
                                                                                   resize_keyboard=True))
        if context.user_data.get("joined_in_settings") or context.user_data.get("selecting_lang"):
            context.user_data["joined_in_settings"] = False
            context.user_data["selecting_lang"] = False
    elif user_message_text == "⚙️ تنظیمات" or user_message_text == "⚙️ Settings":
        await join_in_settings(update, context)
    elif user_message_text == "📋 My Subscription" or user_message_text == "📋 اشتراک من":
        await update.message.reply_text(format_subscription_data(get_user_subscription_data(user_id=user.id), user.id))
    elif context.user_data.get("joined_in_settings"):
        if user_message_text == "Change Language" or user_message_text == "تغییر زبان":
            await join_in_selecting_lang(update, context)
            context.user_data["joined_in_settings"] = False
        else:
            user_lang = get_user_lang(user_id=user.id)
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
    elif get_user_lang(user_id=user.id) == "not_selected":
        context.user_data['selecting_lang'] = True
        await update.message.reply_text(f"{persian.restart}\n\n{english.restart}")
    else:
        user_lang = get_user_lang(user_id=user.id)
        response = persian.didnt_understand if user_lang == "fa" else english.didnt_understand
        await update.message.reply_text(response, quote=True)
