import datetime

from bot.database import users_collection
from bot.users.settings.language import join_in_selecting_lang
from langs import persian, english
from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import ContextTypes
from utils.buttons import homepage_buttons
from utils.is_channel_sub import check_sub


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_data = {"user_id": user.id, "user_name": user.username, "user_firstname": user.first_name,
                 "user_lastname": user.last_name,
                 "registered_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 "subscription": {"type": "free", "status": "active",
                                  "start_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                  "renewal_date": None, "auto_renew": False, "max_size_per_file": 100,
                                  "max_size_per_month": 500, "used_size": 0, "remaining_size": 500,
                                  "features": ["Ads", "Limited to 100mb per video", "Limited to max 500mb per month"],
                                  "history": [{"event_type": "subscription_created",
                                               "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                               "details": "User updgraded to free subscription"}]}, "downloads": [],
                 "settings": {"language": "not_selected"

                              }}
    the_user = users_collection.find_one({"user_id": user.id})
    if not await check_sub(update, context, user.id):
        await update.message.reply_text(f"Please subscribe and then use /start.\n @diardev")
    elif not the_user:
        users_collection.insert_one(user_data)
        await join_in_selecting_lang(update, context)
    elif the_user["settings"]["language"] == "not_selected":
        await join_in_selecting_lang(update, context)
    else:
        languages = {'fa': persian.greeting, 'en': english.greeting}
        selected_lang = the_user["settings"]["language"]
        await update.message.reply_text(languages[selected_lang],
                                        reply_markup=ReplyKeyboardMarkup(homepage_buttons(user.id),
                                                                         resize_keyboard=True))
