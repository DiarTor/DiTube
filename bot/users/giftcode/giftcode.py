import datetime
import secrets
import string

import telebot.types
from bot.database import giftcodes_collection, users_collection
from utils.buttons import homepage_buttons
from utils.get_user_data import get_user_lang_and_return_response
from langs import persian
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
            response = get_user_lang_and_return_response(user.id, persian=persian.redeem_successful)
            users_collection.update_one({"user_id": user.id}, {"$inc": {"balance": code_db["credit"]}})
            bot.send_message(chat_id=msg.chat.id,
                             text=response.format(
                                 users_collection.find_one({"user_id": user.id})["balance"]), reply_markup=homepage_buttons(user.id))
            giftcodes_collection.update_one({"code": code}, {"$set": {"used": True}})
            users_collection.update_one({"user_id": user.id}, {"$set": {"metadata.redeeming_code": False}})
        else:
            response = get_user_lang_and_return_response(user.id, persian=persian.code_already_redeemed)
            bot.send_message(chat_id=msg.chat.id, text=response)
    else:
        response = get_user_lang_and_return_response(user.id, persian=persian.invalid_giftcode)
        bot.send_message(chat_id=msg.chat.id, text=response)
