import telegram
from bot.database import users_collection
from bot.handlers.lang_handler import join_in_selecting_lang
from langs import persian, english
from telegram import Update
from telegram.ext import ContextTypes
from utils.is_channel_sub import check_sub

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_data = {
        "user_id": user.id,
        "user_name": user.username,
        "user_firstname": user.first_name,
        "user_lastname": user.last_name,
        "lang": "not_selected",
        "is_staff": False,
        "premium_plan": "free",
        "allowed_to_download_size": 200,
        "donwloaded_size": 0,
        "premium_time": 0,
    }
    the_user = users_collection.find_one({"user_id": user.id})
    if not await check_sub(update, context, user.id):
        await update.message.reply_text(f"Please subscribe and then use /start.\n @diardev")
    elif not the_user:
        users_collection.insert_one(user_data)
    elif the_user == "not_selected":
        await join_in_selecting_lang(update, context)
    else:
        languages = {
            'fa': persian.greeting,
            'en': english.greeting
        }
        selected_lang = the_user['lang']
        await update.message.reply_text(languages[selected_lang])
