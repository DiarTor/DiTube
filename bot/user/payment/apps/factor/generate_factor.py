import random

import jdatetime
import telebot
from bot.common.button_utils import KeyboardMarkupGenerator
from config.database import factors_collection, users_collection
from languages import persian


class GenerateFactor:
    def __init__(self):
        self.factors_gp = -4032391882
        self.factors_collection = factors_collection
        self.users_collection = users_collection

    def create_factor(self, msg: telebot.types.Message, bot: telebot.TeleBot, user_id: int, price: int,
                      payment_method: str, operation: str) -> None:
        """
        Create a new factor
        :param msg: telebot.types.Message instance
        :param bot: telebot.TeleBot instance
        :param user_id: The user id
        :param price: The price of the factor
        :param payment_method: The payment method
        :return:
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
            "payment_method": payment_method
        }
        factors_collection.insert_one(data)
        factor = factors_collection.find_one({"id": data["id"]})
        response = persian.factors[payment_method]
        formatted_price = "{:,}".format(factor["price"])
        response = response.format(factor["id"], formatted_price)
        bot.edit_message_text(response, msg.chat.id, message_id=msg.message_id, parse_mode="markdown")
        self.send_factor_to_admins(msg, bot, user_id, f"@{user_username}", factor, operation)

    def send_factor_to_admins(self, msg: telebot.types.Message, bot: telebot.TeleBot, user_id: int, username: str,
                              factor: dict, operation: str) -> None:
        """
        Sends a factor to admins.

        :param msg: The message object.
        :param bot: The bot object.
        :param user_id: The user ID.
        :param username: The username.
        :param factor: The factor information.
        :param operation: The operation name.
        """
        response = persian.factors['send_to_admins']
        formatted_price = "{:,}".format(factor["price"])
        keyboard = KeyboardMarkupGenerator(user_id).send_factor_to_admins_buttons(factor_id=factor["id"])
        response = response.format(operation, factor['payment_method'], factor['id'], user_id, username,
                                   formatted_price, factor['created_date_time'], factor['status'])
        bot.send_message(chat_id=self.factors_gp, text=response, reply_markup=keyboard, parse_mode="markdown")
