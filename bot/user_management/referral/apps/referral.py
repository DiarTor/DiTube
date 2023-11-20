import re

import telebot
from config.database import users_collection


def referral_handler(msg: telebot.types.Message, bot: telebot.TeleBot, referral_user_id: int):
    the_user = users_collection.find_one({"user_id": msg.from_user.id})
    user_id = msg.from_user.id
    referral_code_match = re.search(r"ref_(\d+)", msg.text)
    if referral_code_match:
        # referral_code = the user who sent the referral link
        referral_code = int(referral_code_match.group(1))
        if the_user and not the_user.get("referraled"):
            referral_user = users_collection.find_one({"user_id": referral_code})
            if referral_user and user_id != referral_code and referral_code not in referral_user.get("referrals", []):
                users_collection.update_one({"user_id": referral_code}, {"$push": {"referrals": user_id}})
                users_collection.update_one({"user_id": user_id}, {"$set": {"referraled": referral_code}})
                if referral_user.get("referrals", []).count(user_id) % 10 == 0 and referral_user.get("referrals", []).count(user_id) != 1:
                    users_collection.update_one({"user_id": referral_code}, {"$inc": {"balance": 50000}})
                    users_collection.update_one({"user_id": referral_code}, {"$inc": {"referral_total_profit": 50000}})
            else:
                bot.reply_to(msg, "Invalid referral code")
        else:
            bot.reply_to(msg, "You've already used a referral code.")
