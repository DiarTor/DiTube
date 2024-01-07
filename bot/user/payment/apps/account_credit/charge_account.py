import telebot
from bot.common.button_utils import KeyboardMarkupGenerator
from bot.user.account.apps.my_account import MyAccount
from bot.user.utils.user_utils import UserManager
from config.database import factors_collection, users_collection
from languages import persian


class ChargeAccount:
    """
    This handles charge account feature
    """

    def __init__(self):
        self.factors_collection = factors_collection
        self.users_collection = users_collection

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
