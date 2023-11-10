import telebot.types
from bot.database import users_collection
from utils.buttons import settings_buttons
from utils.get_user_data import get_user_lang, get_user_lang_and_return_response
from langs import persian

def join_in_settings(msg: telebot.types.Message, bot: telebot.TeleBot):
    user = msg.from_user
    users_collection.update_one(filter={"user_id": user.id}, update={"$set": {"metadata.joined_in_settings": True}})
    user_lang = get_user_lang(user.id)
    response = get_user_lang_and_return_response(user.id, persian=persian.joined_in_settings)
    bot.send_message(msg.chat.id, response,
                     reply_markup=settings_buttons(user.id))
