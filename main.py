import logging
import threading

import telebot
from bot.common.utils import modify_daily_data
from bot.handlers.callback_handler import CallbackHandler
from bot.handlers.message_handler import MessageHandler
from bot.handlers.start_handler import StartCommandHandler
from bot.user_management.admin.giftcode import generate_code
from bot.user_management.admin.bot_stats import BotStats
from config.token import bot_token

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(bot_token)

bot.register_message_handler(StartCommandHandler().process_start_command, commands=["start"], pass_bot=True)
bot.register_message_handler(generate_code, commands=['gift'], pass_bot=True)
bot.register_message_handler(BotStats().get_bot_stats, commands=['stat'], pass_bot=True)
bot.register_message_handler(BotStats().include_user_balance, commands=['inc_balance'], pass_bot=True)
bot.register_message_handler(BotStats().get_user_stat, commands=['user_stat'], pass_bot=True)
bot.register_message_handler(MessageHandler().handle_message, content_types=['text'], pass_bot=True)
bot.register_message_handler(MessageHandler().handle_photo, content_types=['photo'], pass_bot=True)

bot.register_callback_query_handler(CallbackHandler().process_callback, pass_bot=True, func=lambda call: True)

if __name__ == "__main__":
    reset_thread = threading.Thread(target=modify_daily_data)
    reset_thread.start()
    bot.infinity_polling()
