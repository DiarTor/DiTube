import datetime
import re
import asyncio
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
    the_user = users_collection.find_one({"user_id": user.id})
    if not the_user:
        # New user: Insert user data into the database
        user_data = {
            "user_id": user.id,
            "user_name": user.username,
            "user_firstname": user.first_name,
            "user_lastname": user.last_name,
            "balance": 0,
            "referrals": [],
            "referraled": None,  # Store the referrer's user ID
            "registered_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_download_time": {},
            "subscription": {
                "type": "bronze",
                "status": "active",
                "price": 0,
                "start_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "expire_date": None,
                "auto_renew": False,
                "max_file_size": 200,
                "max_data_per_day": 1000,
                "used_data": 0,
                "remaining_data": 500,
                "last_reset_date": datetime.date.today().strftime("%Y-%m-%d"),
                "history": [
                    {
                        "event_type": "subscription_created",
                        "subscription_type": "bronze",
                        "price": 0,
                        "subscription_date": "",
                        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "details": "User upgraded to free subscription",
                    }
                ],
            },
            "downloads": [],
            "settings": {
                "language": "not_selected",
            },
        }
        users_collection.insert_one(user_data)
        the_user = users_collection.find_one({"user_id": user.id})

    if context.args and the_user["settings"]["language"] == "not_selected":
        referral_code_match = re.match(r'ref_(\w+)', context.args[0])
        if referral_code_match:
            referral_code = int(referral_code_match.group(1))
            if the_user and not the_user.get("referraled"):
                referral_user = users_collection.find_one({"user_id": referral_code})
                if referral_user and user.id != referral_code and referral_code not in referral_user.get("referrals", []):
                    # Update referrer and referred users
                    users_collection.update_one({"user_id": referral_code}, {"$push": {"referrals": user.id}})
                    users_collection.update_one({"user_id": user.id}, {"$set": {"referraled": referral_code}})
                else:
                    await update.message.reply_text("Invalid referral code")
            else:
                await update.message.reply_text("You've already used a referral code.")
    if not await check_sub(update, context, user.id):
        await update.message.reply_text("Please subscribe and then use /start. @diardev")
        return
    if the_user["settings"]["language"] == "not_selected":
        await join_in_selecting_lang(update, context)
    else:
        languages = {'fa': persian.greeting, 'en': english.greeting}
        selected_lang = the_user["settings"]["language"]
        await update.message.reply_text(languages[selected_lang],
                                        reply_markup=ReplyKeyboardMarkup(homepage_buttons(user.id),
                                                                         resize_keyboard=True))

