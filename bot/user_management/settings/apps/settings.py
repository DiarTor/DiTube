import telebot.types
from config.database import users_collection
from languages import persian
from bot.user_management.utils.button_utils import KeyboardMarkupGenerator
from bot.user_management.utils.user_utils import UserManager


def join_in_settings(msg: telebot.types.Message, bot: telebot.TeleBot):
    user = msg.from_user
    users_collection.update_one(filter={"user_id": user.id}, update={"$set": {"metadata.joined_in_settings": True}})
    response = UserManager(user.id).return_response_based_on_language(persian=persian.joined_in_settings)
    bot.send_message(msg.chat.id, response,
                     reply_markup=KeyboardMarkupGenerator(user.id).settings_buttons())