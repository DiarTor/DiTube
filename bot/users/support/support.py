import re

import telebot.types
from bot.database import users_collection
from langs import persian
from utils.button_utils import KeyboardMarkupGenerator
from utils.user_utils import UserManager


def join_in_support(msg: telebot.types.Message, bot: telebot.TeleBot):
    response = UserManager(msg.from_user.id).return_response_based_on_language(
        persian=persian.youre_connected_to_support)
    users_collection.update_one({'user_id': msg.from_user.id}, {'$set': {"metadata.joined_in_support": True}})
    bot.send_message(msg.chat.id, response,
                     reply_markup=KeyboardMarkupGenerator(msg.from_user.id).return_buttons())


def send_user_msg_to_support(msg: telebot.types.Message, bot: telebot.TeleBot):
    support_group_id = -4043182903
    response = UserManager(msg.from_user.id).return_response_based_on_language(
        persian=persian.your_message_was_sent_to_support)
    bot.send_message(chat_id=support_group_id,
                     text=f"Username: {msg.from_user.username}\nUser ID: `{msg.from_user.id}`\nChat ID : `{msg.chat.id}`\nMessage:\n\n {msg.text}",
                     parse_mode="Markdown")
    bot.send_message(chat_id=msg.chat.id, text=response,
                     reply_markup=KeyboardMarkupGenerator(msg.from_user.id).homepage_buttons())
    users_collection.update_one({'user_id': msg.from_user.id}, {'$set': {"metadata.joined_in_support": False}})


def send_user_photo_to_support(msg: telebot.types.Message, bot: telebot.TeleBot):
    support_group_id = -4043182903
    response = UserManager(msg.from_user.id).return_response_based_on_language(
        persian=persian.your_message_was_sent_to_support)
    bot.send_photo(chat_id=support_group_id, photo=msg.photo[-1].file_id,
                   caption=f"Username: {msg.from_user.username}\nUser ID: `{msg.from_user.id}`\nChat ID : `{msg.chat.id}`",
                   parse_mode="Markdown")
    bot.send_message(chat_id=msg.chat.id, text=response,
                     reply_markup=KeyboardMarkupGenerator(msg.from_user.id).homepage_buttons())
    users_collection.update_one({'user_id': msg.from_user.id}, {'$set': {"metadata.joined_in_support": False}})


def reply_to_user_support_msg(msg: telebot.types.Message, bot: telebot.TeleBot):
    reply_response_template = UserManager(msg.from_user.id).return_response_based_on_language(
        persian=persian.reciving_message_from_support)
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
            bot.send_message(chat_id=chat_id, text=f"{reply_response_template}\n\n{msg.text}")
        elif msg.photo:
            if msg.caption:
                caption = msg.caption
            else:
                caption = ""
            bot.send_photo(chat_id=chat_id, photo=msg.photo[-1].file_id,
                           caption=f"{reply_response_template}\n\n{caption}")
