import datetime
import re

import telebot.types
from bot.database import users_collection
from bot.users.settings.language import join_in_selecting_lang
from langs import english, persian
from utils.buttons import homepage_buttons
from utils.is_channel_sub import check_sub


def start(msg: telebot.types.Message, bot: telebot.TeleBot):
    user = msg.from_user
    the_user = users_collection.find_one({"user_id": user.id})
    if not the_user:
        user_data = {
            "user_id": user.id,
            "user_name": user.username,
            "user_firstname": user.first_name,
            "user_lastname": user.last_name,
            "balance": 0,
            "referrals": [],
            "referraled": None,
            "registered_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "subscription": {
                "type": "bronze",
                "status": "active",
                "price": 0,
                "start_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "expire_date": None,
                "auto_renew": False,
                "max_file_size": 200,
                "max_data_per_day": 800,
                "used_data": 0,
                "remaining_data": 800,
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
            "metadata": {
                "selecting_language": False,
                "joined_in_settings": False


            },
        }
        users_collection.insert_one(user_data)
        the_user = users_collection.find_one({"user_id": user.id})
    args = msg.text.split()[1:]
    if args and the_user["settings"]["language"] == "not_selected":
        referral_code_match = re.match(r'ref_(\w+)', args[0])
        if referral_code_match:
            referral_code = int(referral_code_match.group(1))
            if the_user and not the_user.get("referraled"):
                referral_user = users_collection.find_one({"user_id": referral_code})
                if referral_user and user.id != referral_code and referral_code not in referral_user.get("referrals",
                                                                                                         []):
                    # Update referrer and referred users
                    users_collection.update_one({"user_id": referral_code}, {"$push": {"referrals": user.id}})
                    users_collection.update_one({"user_id": user.id}, {"$set": {"referraled": referral_code}})
                else:
                    bot.reply_to(msg, "Invalid referral code")
            else:
                bot.reply_to(msg, "You've already used a referral code.")
    if not check_sub(msg, bot):
        bot.reply_to(msg, "Please subscribe and then use /start. @diardev")
        return
    if the_user["settings"]["language"] == "not_selected":
        join_in_selecting_lang(msg, bot)
    else:
        languages = {'fa': persian.greeting, 'en': english.greeting}
        selected_lang = the_user["settings"]["language"]
        bot.send_message(chat_id=msg.chat.id, text=languages[selected_lang],
                         reply_markup=homepage_buttons(user.id))
