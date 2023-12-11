import datetime
import secrets
import string

import telebot.types
from bot.common.button_utils import KeyboardMarkupGenerator
from bot.user_management.utils.user_utils import UserManager
from config.database import giftcodes_collection, users_collection
from languages import persian, english


def generate_code(msg: telebot.types.Message, bot: telebot.TeleBot):
    admin = 1154909190
    if msg.from_user.id == admin:
        code = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(10))
        try:
            credit = msg.text.split()[1]
        except IndexError:
            credit = None
        if not credit:
            bot.send_message(chat_id=msg.chat.id, text="Please specify a credit amount. /gift <credit>")
            return
        giftcodes_collection.insert_one(
            {"code": code, "credit": int(credit), "created_by": msg.from_user.id, "used": False,
             "used_by": None,
             "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        bot.send_message(chat_id=msg.chat.id,
                         text=f"The Code Generated Successfuly !\nYour code : `{code}`\nCredit : {credit} Toman",
                         parse_mode="Markdown")
    else:
        pass


def redeem_giftcode(msg: telebot.types.Message, bot: telebot.TeleBot):
    user = msg.from_user
    code = msg.text
    code_db = giftcodes_collection.find_one({"code": code})
    format_number_with_commas = lambda number: f"{number:,}"
    if code_db:
        if code_db["used"] == False:
            users_collection.update_one({"user_id": user.id}, {"$inc": {"balance": code_db["credit"]}})
            user_new_balance = users_collection.find_one({"user_id": user.id})["balance"]
            giftcodes_collection.update_one({"code": code}, {"$set": {"used": True, "used_by": user.id}})
            users_collection.update_one({"user_id": user.id}, {"$set": {"metadata.redeeming_code": False}})
            response = UserManager(user.id).return_response_based_on_language(persian=persian.redeem_successful,
                                                                              english=english.redeem_successful)
            user_new_balance = format_number_with_commas(user_new_balance)
            response = response.format(user_new_balance)
            bot.send_message(chat_id=msg.chat.id,
                             text=response,
                             reply_markup=KeyboardMarkupGenerator(user.id).homepage_buttons(), parse_mode="Markdown")
        else:
            response = UserManager(user.id).return_response_based_on_language(persian=persian.code_already_redeemed,
                                                                              english=english.code_already_redeemed)
            bot.send_message(chat_id=msg.chat.id, text=response)
    else:
        response = UserManager(user.id).return_response_based_on_language(persian=persian.invalid_giftcode,
                                                                          english=english.invalid_giftcode)
        bot.send_message(chat_id=msg.chat.id, text=response)
