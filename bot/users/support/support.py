import telebot.types
from bot.database import users_collection
from utils.buttons import homepage_buttons, return_buttons
import re

def join_in_support(msg: telebot.types.Message, bot: telebot.TeleBot):
    users_collection.update_one({'user_id': msg.from_user.id}, {'$set': {"metadata.joined_in_support": True}})
    bot.send_message(msg.chat.id, "Youre now conected to support section, please send your message",
                     reply_markup=return_buttons(msg.from_user.id))


def send_user_msg_to_support(msg: telebot.types.Message, bot: telebot.TeleBot):
    support_group_id = -4043182903
    bot.send_message(chat_id=support_group_id,
                     text=f"Username: {msg.from_user.username}\nUser ID: `{msg.from_user.id}`\nChat ID : `{msg.chat.id}`\nMessage:\n\n {msg.text}", parse_mode="Markdown")
    bot.send_message(chat_id=msg.chat.id, text="Your message has been sent to support",
                     reply_markup=homepage_buttons(msg.from_user.id))
    users_collection.update_one({'user_id': msg.from_user.id}, {'$set': {"metadata.joined_in_support": False}})


def send_user_photo_to_support(msg: telebot.types.Message, bot: telebot.TeleBot):
    support_group_id = -4043182903
    bot.send_photo(chat_id=support_group_id, photo=msg.photo[-1].file_id,
                   caption=f"Username: {msg.from_user.username}\nUser ID: `{msg.from_user.id}`\nChat ID : `{msg.chat.id}`", parse_mode="Markdown")
    bot.send_message(chat_id=msg.chat.id, text="Your photo has been sent to support",
                     reply_markup=homepage_buttons(msg.from_user.id))
    users_collection.update_one({'user_id': msg.from_user.id}, {'$set': {"metadata.joined_in_support": False}})

def reply_to_user_support_msg(msg: telebot.types.Message, bot: telebot.TeleBot):
    reply_response = msg.reply_to_message
    if reply_response.text:
        reply_response = reply_response.text
    elif reply_response.caption:
        reply_response = reply_response.caption
    chat_id_match = re.search(r'Chat ID :\s*(\d+)', reply_response)
    if chat_id_match:
        chat_id = chat_id_match.group(1)
        chat_id = chat_id.strip()
        if msg.text:
            bot.send_message(chat_id=chat_id, text=f"Message from Support:\n\n{msg.text}")
        elif msg.photo:
            if msg.caption:
                caption = msg.caption
            else:
                caption = ""
            bot.send_photo(chat_id=chat_id, photo=msg.photo[-1].file_id, caption=f"Message from Support:\n\n{caption}")


