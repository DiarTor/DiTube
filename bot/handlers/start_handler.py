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
                 "last_download_time": {},
                 "subscription": {"type": "bronze", "status": "active",
                                  "price": 0,
                                  "start_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                  "expire_date": None, "auto_renew": False, "max_file_size": 200,
                                  "max_data_per_day": 1000, "used_data": 0, "remaining_data": 500,
                                  "last_reset_date": datetime.date.today().strftime("%Y-%m-%d"),
                                  "history": [{"event_type": "subscription_created",
                                               "subscription_type": "bronze",
                                               "price": 0,
                                               "subscription_date": "",
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
