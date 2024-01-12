import jdatetime
import telebot
from config.database import factors_collection, users_collection
from languages import persian


class HandleFactor:
    def __init__(self):
        self.factors_gp = -4032391882
        self.factors_collection = factors_collection
        self.users_collection = users_collection
        self.date_time = self._get_date_time()
        self.date = self._get_date()
        self.time = self._get_time()

    def _get_date_time(self):
        return jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    def _get_date(self):
        return jdatetime.date.today().strftime("%Y/%m/%d")

    def _get_time(self):
        return jdatetime.datetime.now().strftime("%H:%M:%S")

    def confirm_charge_factor(self, msg: telebot.types.Message, bot: telebot.TeleBot, factor_id: int,
                              callback_id: int) -> None:
        """
        Confirms a charge account factor and sends a response to the user.
        :param msg: The message object.
        :param bot: The bot object.
        :param factor_id: The factor ID.
        :param callback_id: The callback ID.
        """
        # Find the factor with the given factor_id
        factor = self.factors_collection.find_one({"id": factor_id})

        # Find the user associated with the factor
        user = self.users_collection.find_one({"user_id": factor['user_id']})
        user_id = user['user_id']
        user_username = user['user_name']

        # Check if the factor status is already confirmed or denied
        status = factor['status']
        if status in {"confirmed", "denied"}:
            bot.answer_callback_query(callback_id, text=persian.this_factor_already[status], show_alert=True)
            return

        # Update the factor and user balance
        factor_price_to_toman = factor['price'] // 10
        filter = {"id": factor_id}
        self.factors_collection.update_one({"id": factor_id}, {
            "$set": {"status": "confirmed", "check_date_time": self.date_time, "check_date": self.date,
                     "check_time": self.time, "check_method": "manual"}})
        self.users_collection.update_one({"user_id": user_id},
                                         {"$inc": {"balance": factor_price_to_toman}})

        # Generate the response message
        response = persian.charge_account_factor_confired
        formatted_price = "{:,}".format(factor["price"] // 10)
        response = response.format(factor_id, formatted_price)

        # Reply to the message with a confirmation message in the admins group
        bot.reply_to(msg, "✅این فاکتور تایید شد.", parse_mode="markdown")

        # Send the response message to the user
        bot.send_message(chat_id=user_id, text=response, parse_mode="markdown")

    def deny_charge_factor(self, msg: telebot.types.Message, bot: telebot.TeleBot, factor_id: int,
                           callback_id: int) -> None:
        """
        Denies a charge account factor and sends a response to the user.
        :param msg: The message object.
        :param bot: The bot object.
        :param factor_id: The factor ID.
        :param callback_id: The callback ID.
        :return:
        """
        # Find the factor with the given factor_id
        factor = self.factors_collection.find_one({"id": factor_id})

        # Find the user associated with the factor
        user = self.users_collection.find_one({"user_id": factor['user_id']})

        # Get the user's id and username
        user_id = user['user_id']
        user_username = user['user_name']

        # Check if the factor status is already confirmed or denied
        status = factor['status']
        if status in {"confirmed", "denied"}:
            bot.answer_callback_query(callback_id, text=persian.this_factor_already[status], show_alert=True)
            return

        # Update the status of the factor to "denied"
        self.factors_collection.update_one({"id": factor_id}, {"$set": {"status": "denied"}})

        # Generate the response message
        response = persian.charge_account_factor_denied
        response = response.format(factor_id)

        # Reply to the original message with a denial notification
        bot.reply_to(msg, "❌این فاکتور رد شد.", parse_mode="markdown")

        # Send the response message to the user
        bot.send_message(chat_id=user_id, text=response, parse_mode="markdown")
