import logging
import threading

import telebot
from bot.handlers import start_handler, message_handler, callback_handler
from bot.user_management.giftcode.apps import giftcode
from bot.common.utils import reset_daily_data

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot("6545347914:AAF0-kxh-8Ztn8JNXTCkmiumfdR3Z7K8vKs")

bot.register_message_handler(start_handler.start, commands=["start"], pass_bot=True)
bot.register_message_handler(giftcode.generate_code, commands=['ggift'], pass_bot=True)
bot.register_message_handler(message_handler.handle_user_message, content_types=['text'], pass_bot=True)
bot.register_message_handler(message_handler.handle_user_photo, content_types=['photo'], pass_bot=True)
bot.register_callback_query_handler(callback_handler.handle_callback, pass_bot=True, func=lambda call: True)


if __name__ == "__main__":
    reset_thread = threading.Thread(target=reset_daily_data)
    reset_thread.start()
    bot.infinity_polling()
