import random

import telebot
from bot.common.button_utils import KeyboardMarkupGenerator
from bot.user_management.account.apps.my_account import MyAccount
from bot.user_management.utils.user_utils import UserManager
from config.database import factors_collection
from languages import persian
from persiantools.jdatetime import JalaliDateTime


class ChargeAccount:
    def send_factor_to_admins(self, msg: telebot.types.Message, bot: telebot.TeleBot, user_id, username, factor):
        factors_manager_gp = -4032391882
        response = UserManager(user_id).return_response_based_on_language(persian=persian.send_factor_message_to_admin)
        keyboard = KeyboardMarkupGenerator(user_id).send_factor_to_admins_buttons(price=factor['price'],
                                                                                  factor_id=factor['id'],
                                                                                  user_id=user_id)
        formatted_price = f"{factor['price']:,}"
        response = response.format("شارژ اکانت", factor['method'], factor['id'], user_id, username,
                                   formatted_price, factor['created_date'],factor['status'])
        bot.send_message(chat_id=factors_manager_gp, text=response, reply_markup=keyboard, parse_mode="markdown")

    def handle_return(self, msg: telebot.types.Message, bot: telebot.TeleBot, user_id, return_to):
        if return_to == 'return_to_my_account':
            kb = KeyboardMarkupGenerator(user_id).account_buttons()
            response = MyAccount().return_only_user_details_response(user_id=user_id)
            bot.edit_message_text(response, msg.chat.id, message_id=msg.message_id, reply_markup=kb,
                                  parse_mode="markdown")
        elif return_to == 'return_to_charge_methods':
            self.show_charge_methods(msg, bot, user_id)

    def show_charge_methods(self, msg: telebot.types.Message, bot: telebot.TeleBot, user_id):
        user_manager = UserManager(user_id)
        kb = KeyboardMarkupGenerator(user_id).charge_account_methods_buttons()
        response = user_manager.return_response_based_on_language(persian=persian.charge_account_methods)
        bot.edit_message_text(response, msg.chat.id, message_id=msg.message_id, reply_markup=kb)

    def show_plans_list(self, msg: telebot.types.Message, bot: telebot.TeleBot, method, user_id):
        kb = KeyboardMarkupGenerator(user_id).charge_account_plans_buttons(method)
        response = UserManager(user_id).return_response_based_on_language(persian=persian.charge_account_plans)
        bot.edit_message_text(response, msg.chat.id, message_id=msg.message_id, reply_markup=kb)

    def generate_factor_card_to_card(self, msg: telebot.types.Message, bot: telebot.TeleBot, price, user_id):
        iranian_time = JalaliDateTime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "id": random.Random().randint(100000, 999999),
            "user_id": user_id,
            "price": price * 10,
            "type": "charge_account",
            "created_date": iranian_time,
            "status": "pending",
            "confirmed": False,
            "confirm_date": None,
            "deny_date": None,
            "confirm_method": None,
            "method": "card_to_card",
        }
        factors_collection.insert_one(data)
        factor = factors_collection.find_one({"id": data["id"]})
        response = UserManager(user_id).return_response_based_on_language(persian=persian.card_to_card_factor)
        formatted_price = "{:,}".format(factor["price"])
        response = response.format(factor["id"], formatted_price)
        bot.edit_message_text(response, msg.chat.id, message_id=msg.message_id, parse_mode="markdown")
        self.send_factor_to_admins(msg, bot, user_id, msg.from_user.username, factor)
