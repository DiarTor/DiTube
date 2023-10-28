from telebot.types import Message
from telebot import TeleBot


def check_sub(msg: Message, bot: TeleBot):
    channel_id = -1001594818741
    chat_member = bot.get_chat_member(chat_id=channel_id, user_id=msg.from_user.id)
    if chat_member.status in ["member", "administrator", "creator"]:
        return True
    return False
