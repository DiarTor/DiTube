from urllib.error import HTTPError, URLError

import telebot.types
from bot.database import users_collection
from bot.download_videos.get_video_information import get_video_options, get_only_filesize
from langs import persian, english
from pytube import YouTube
from pytube.exceptions import AgeRestrictedError
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def youtube_video_handler(msg: telebot.types.Message, bot: telebot.TeleBot):
    user = msg.from_user
    user_message_text = msg.text
    chat_id = msg.chat.id
    user_lang = users_collection.find_one({"user_id": user.id})["settings"]["language"]
    geting_info_response = persian.get_video_info if user_lang == "fa" else english.get_video_info
    message_info = bot.send_message(chat_id, geting_info_response, reply_to_message_id=msg.message_id)
    kb = []
    yt = YouTube(user_message_text)
    try:
        video_options = get_video_options(yt)
        sorted_video_options = sorted(video_options, key=lambda x: int(x.split()[0].split('p')[0]), reverse=True)
    except (AgeRestrictedError, HTTPError, URLError) as e:
        if HTTPError:
            print(e)
            bot.send_message(chat_id, "An error occurred. Please try again later.",
                             reply_to_message_id=msg.message_id)
            return
        elif AgeRestrictedError:
            bot.send_message(chat_id, response, reply_to_message_id=msg.message_id)
            return
        elif URLError:
            bot.send_message(chat_id, "bad url", reply_to_message_id=msg.message_id)
    for item in video_options:
        parts = item.split()
        if len(parts) == 2:
            quality, size = parts
            kb.append([InlineKeyboardButton(f"{quality} {size}",
                                            callback_data=f"{yt.video_id} {quality} {chat_id}")])

    if user_lang == "en":
        audio_file_size = get_only_filesize(user_message_text)
        formatted_size = "{:.1f} MB".format(audio_file_size)
        kb.append([InlineKeyboardButton(f"Download Audio ({formatted_size} mb)",
                                        callback_data=f"{yt.video_id} vc {chat_id}")])
    else:
        audio_file_size = get_only_filesize(user_message_text)
        formatted_size = "{:.1f} MB".format(audio_file_size)
        kb.append(
            [InlineKeyboardButton(f"دانلود صدا ({formatted_size} mb)", callback_data=f"{yt.video_id} vc {chat_id}")])
    reply_markup = InlineKeyboardMarkup(kb)
    response = persian.select_quality if user_lang == "fa" else english.select_quality
    bot.send_message(chat_id, response, reply_markup=reply_markup, reply_to_message_id=msg.message_id)
    bot.delete_message(chat_id, message_info.id)


def youtube_shorts_handler(msg: telebot.types.Message, bot: telebot.TeleBot):
    ususer = msg.from_user
    user_message_text = msg.text
    chat_id = msg.chat.id
    user_lang = users_collection.find_one({"user_id": user.id})["settings"]["language"]
    geting_info_response = persian.get_video_info if user_lang == "fa" else english.get_video_info
    message_info = bot.send_message(chat_id, geting_info_response, reply_to_message_id=msg.message_id)
    kb = []
    yt = YouTube(user_message_text)
    try:
        video_options = get_video_options(yt)
    except (AgeRestrictedError, HTTPError):
        if HTTPError:
            bot.send_message(chat_id, "An error occurred. Please try again later.",
                             reply_to_message_id=msg.message_id)
            return
        elif AgeRestrictedError:
            bot.send_message(chat_id, response, reply_to_message_id=msg.message_id)
            return
    for item in sorted(video_options, reverse=True):
        parts = item.split()
        if len(parts) == 2:
            quality, size = parts
            kb.append([InlineKeyboardButton(f"{quality} {size}",
                                            callback_data=f"{yt.video_id} {quality} {chat_id}")])
    reply_markup = InlineKeyboardMarkup(kb)
    response = persian.select_quality if user_lang == "fa" else english.select_quality
    bot.send_message(chat_id, response, reply_markup=reply_markup, reply_to_message_id=msg.message_id)
    message_info.delete()
