import logging
import threading

import telebot
from bot.user_management.account.apps import giftcode
from bot.common.utils import modify_daily_data
from bot.handlers.start_handler import StartCommandHandler
from bot.handlers.message_handler import MessageHandler
from bot.handlers.callback_handler import CallbackHandler

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot("6545347914:AAF0-kxh-8Ztn8JNXTCkmiumfdR3Z7K8vKs")

bot.register_message_handler(StartCommandHandler().process_start_command, commands=["start"], pass_bot=True)
bot.register_message_handler(giftcode.generate_code, commands=['gift'], pass_bot=True)
bot.register_message_handler(MessageHandler().handle_message, content_types=['text'], pass_bot=True)
bot.register_message_handler(MessageHandler().handle_photo, content_types=['photo'], pass_bot=True)

bot.register_callback_query_handler(CallbackHandler().process_callback, pass_bot=True, func=lambda call: True)


if __name__ == "__main__":
    reset_thread = threading.Thread(target=modify_daily_data)
    reset_thread.start()
    bot.infinity_polling()
