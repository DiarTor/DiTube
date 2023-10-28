import datetime
import secrets
import string

import telebot.types
from bot.database import giftcodes_collection, users_collection
from utils.buttons import homepage_buttons

def generate_code(msg: telebot.types.Message, bot: telebot.TeleBot):
    admin = 1154909190
    if msg.from_user.id == admin:
        code = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(10))
        try:
            credit = msg.text.split()[1]
        except IndexError:
            credit = None
        if not credit:
            bot.send_message(chat_id=msg.chat.id, text="Please specify a credit amount. /ggift <credit>")
            return
        giftcodes_collection.insert_one(
            {"code": code, "credit": int(credit), "used": False,
             "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        bot.send_message(chat_id=msg.chat.id, text="The Code Generated Successfuly !\nYour code : `{}`\nCredit : {} Toman".format(code, credit), parse_mode="Markdown")
    else:
        pass


def redeem_giftcode(msg: telebot.types.Message, bot: telebot.TeleBot):
    user = msg.from_user
    code = msg.text
    code_db = giftcodes_collection.find_one({"code": code})
    if code_db:
        if code_db["used"] == False:
            users_collection.update_one({"user_id": user.id}, {"$inc": {"balance": code_db["credit"]}})
            bot.send_message(chat_id=msg.chat.id,
                             text="The Code Redeemed Successfuly !\nYour new balance is *{}*.".format(
                                 users_collection.find_one({"user_id": user.id})["balance"]), reply_markup=homepage_buttons(user.id))
            giftcodes_collection.update_one({"code": code}, {"$set": {"used": True}})
            users_collection.update_one({"user_id": user.id}, {"$set": {"metadata.redeeming_code": False}})
        else:
            bot.send_message(chat_id=msg.chat.id, text="This gift code has already been redeemed.")
    else:
        bot.send_message(chat_id=msg.chat.id, text="Invalid gift code.")
