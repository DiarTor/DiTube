import telebot.types
from bot.database import users_collection
from utils.buttons import settings_buttons
from utils.get_user_data import get_user_lang


def join_in_settings(msg: telebot.types.Message, bot: telebot.TeleBot):
    user = msg.from_user
    users_collection.update_one(filter={"user_id": user.id}, update={"$set": {"metadata.joined_in_settings": True}})
    user_lang = get_user_lang(user.id)
    response = "Please Use The Buttons Below " if user_lang == "en" else "لطفا از دکمه های زیر استفاده کنید"
    bot.send_message(msg.chat.id, response,
                     reply_markup=settings_buttons(user.id))
