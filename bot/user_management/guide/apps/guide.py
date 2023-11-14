import telebot.types
from bot.user_management.utils.user_utils import UserManager
from languages import persian
def send_guide_message(msg: telebot.types.Message, bot: telebot.TeleBot):
    response = UserManager(msg.from_user.id).return_response_based_on_language(persian=persian.guide)
    bot.send_message(msg.chat.id, response, parse_mode="Markdown")