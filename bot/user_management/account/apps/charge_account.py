import random

import jdatetime
import telebot
from bot.common.button_utils import KeyboardMarkupGenerator
from bot.user_management.account.apps.my_account import MyAccount
from bot.user_management.utils.user_utils import UserManager
from config.database import factors_collection, users_collection
from languages import persian


class ChargeAccount:
    """
    This handles charge account feature
    """
    def send_factor_to_admins(self, msg: telebot.types.Message, bot: telebot.TeleBot, user_id, username, factor):
        """
        Send the factor details to the admin group
        :param msg: telebot.types.Message instance
        :param bot: telebot.TeleBot instance
        :param user_id: The user id
        :param username: the user telegram username (@example)
        :param factor: the factor instance from the database
        :return:
        """
        factors_manager_gp = -4032391882
        response = persian.send_factor_message_to_admin
        keyboard = KeyboardMarkupGenerator(user_id).send_factor_to_admins_buttons(factor_id=factor['id'])
        formatted_price = f"{factor['price']:,}"
        response = response.format("شارژ اکانت", factor['payment_method'], factor['id'], user_id, username,
                                   formatted_price, factor['created_date_time'], factor['status'])
        bot.send_message(chat_id=factors_manager_gp, text=response, reply_markup=keyboard, parse_mode="markdown")

    def handle_return(self, msg: telebot.types.Message, bot: telebot.TeleBot, user_id, return_to):
        """
        it returns the user to the demaned message
        :param msg: telebot.types.Message instance
        :param bot: telebot.TeleBot instance
        :param user_id: The user id
        :param return_to: the message id you want to return the user to
        :return: it return the user to the demanded message
        """
        if return_to == 'return_to_my_account':
            kb = KeyboardMarkupGenerator(user_id).account_buttons()
            response = MyAccount().return_only_user_details_response(user_id=user_id)
            bot.edit_message_text(response, msg.chat.id, message_id=msg.message_id, reply_markup=kb,
                                  parse_mode="markdown")
        elif return_to == 'return_to_charge_methods':
            self.show_charge_methods(msg, bot, user_id)

    def show_charge_methods(self, msg: telebot.types.Message, bot: telebot.TeleBot, user_id):
        """
        Shows charge account methods
        :param msg: telebot.types.Message instance
        :param bot: telebot.TeleBot instance
        :param user_id: The user id
        :return: List of InlineKeyboard buttons showing charge account methods
        """
        user_manager = UserManager(user_id)
        kb = KeyboardMarkupGenerator(user_id).charge_account_methods_buttons()
        bot.edit_message_text(persian.charge_account_methods, msg.chat.id, message_id=msg.message_id, reply_markup=kb)

    def show_plans_list(self, msg: telebot.types.Message, bot: telebot.TeleBot, method, user_id):
        """
        It shows charge account plans
        :param msg: telebot.types.Message instance
        :param bot: telebot.TeleBot instance
        :param method: the method the user selected to pay for charging account
        :param user_id: The user id
        :return: a list of InlineKeyboard buttons with charge prices
        """
        kb = KeyboardMarkupGenerator(user_id).charge_account_plans_buttons(method)
        bot.edit_message_text(persian.charge_account_plans, msg.chat.id, message_id=msg.message_id, reply_markup=kb)

    def generate_factor_card_to_card(self, msg: telebot.types.Message, bot: telebot.TeleBot, price, user_id):
        """
        it generate a factor with card_to_card method
        :param msg: telebot.types.Message instance
        :param bot: telebot.TeleBot instance
        :param price: the choosen price of the factor
        :param user_id: The user id
        :return: it creates and send the factor if everything is fine
        """
        date_time = jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        user_username = users_collection.find_one({"user_id": user_id})["user_name"]
        data = {
            "id": random.Random().randint(100000, 999999),
            "user_id": user_id,
            "price": price * 10,
            "type": "charge_account",
            "created_date_time": date_time,
            "status": "pending",
            "check_date_time": None,
            "check_date": None,
            "check_time": None,
            "check_method": None,
            "payment_method": "card_to_card",
        }
        factors_collection.insert_one(data)
        factor = factors_collection.find_one({"id": data["id"]})
        response = persian.card_to_card_factor
        formatted_price = "{:,}".format(factor["price"])
        response = response.format(factor["id"], formatted_price)
        bot.edit_message_text(response, msg.chat.id, message_id=msg.message_id, parse_mode="markdown")
        self.send_factor_to_admins(msg, bot, user_id, f"@{user_username}", factor)

    def factor_response(self, msg: telebot.types.Message, bot: telebot.TeleBot, factor_id, status,
                        callback_id):
        """
        Deny or confirm the factor
        :param msg: telebot.types.Message instance
        :param bot: telebot.TeleBot instance
        :param factor_id: the factor id
        :param status: the factor aproval status
        :param callback_id: the callback id
        :return: the factor result (confirmed, denied)
        """
        date_time = jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        date = jdatetime.date.today().strftime("%Y/%m/%d")
        time = jdatetime.datetime.now().strftime("%H:%M:%S")
        factor_id = int(factor_id)
        factor = factors_collection.find_one({"id": factor_id})
        user = users_collection.find_one({"user_id": factor['user_id']})
        user_id = user['user_id']
        user_username = user['user_name']
        if factor['status'] in {"confirmed", "denied"}:
            bot.answer_callback_query(callback_id, text=persian.charge_account_factor_already_confirmed_denined,
                                      show_alert=True)
            return
        if status == "confirm_factor":
            factor_price = factor["price"] // 10
            users_collection.update_one({"user_id": user_id}, {"$inc": {"balance": factor_price}})
            factors_collection.update_one({"id": factor_id}, {
                "$set": {"check_date_time": date_time, "check_date": date, "check_time": time, "status": "confirmed",
                         "check_method": "manual"}})
            response = persian.charge_account_factor_confired
            formatted_price = "{:,}".format(factor_price)
            response = response.format(factor_id, formatted_price)

            bot.reply_to(msg, "✅این فاکتور تایید شد.", parse_mode="markdown")
            bot.send_message(chat_id=user_id, text=response, parse_mode="markdown")
        elif status == "deny_factor":
            factors_collection.update_one({"id": factor_id},
                                          {"$set": {"check_date_time": date_time, "check_date": date,
                                                    "check_time": time, "status": "denied", "check_method": "manual"}})
            response = persian.charge_account_factor_denied
            response = response.format(factor_id)
            bot.reply_to(msg, "❌این فاکتور رد شد.", parse_mode="markdown")
            bot.send_message(chat_id=user_id, text=response, parse_mode="markdown")
