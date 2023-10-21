import time
from urllib.error import HTTPError

from bot.database import users_collection
from bot.download_videos.get_video_information import get_video_options, get_only_filesize
from langs import persian, english
from pytube import YouTube
from pytube.exceptions import AgeRestrictedError
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


async def youtube_video_handler(update, context) -> None:
    user = update.effective_user
    user_message_text = update.message.text
    chat_id = update.effective_chat.id
    user_lang = users_collection.find_one({"user_id": user.id})["settings"]["language"]
    geting_info_response = persian.get_video_info if user_lang == "fa" else english.get_video_info
    message_info = await update.message.reply_text(geting_info_response, quote=True)
    kb = []
    yt = YouTube(user_message_text)
    try:
        video_options = get_video_options(yt)
        sorted_video_options = sorted(video_options, key=lambda x: int(x.split()[0].split('p')[0]), reverse=True)
    except (AgeRestrictedError, HTTPError):
        if HTTPError:
            await update.message.reply_text("An error occurred. Please try again later.")
            return
        elif AgeRestrictedError:
            await update.message.reply_text(persian.age_restricted if user_lang == "fa" else english.age_restricted,
                                            quote=True)
            return
    for item in video_options:
        parts = item.split()
        if len(parts) == 2:
            quality, size = parts
            kb.append([InlineKeyboardButton(f"{quality} {size}",
                                            callback_data=f"{yt.video_id} {quality} {chat_id}")])

    if user_lang == "en":
        audio_file_size = get_only_filesize(user_message_text)
        kb.append([InlineKeyboardButton(f"Download Audio ({audio_file_size} mb)",
                                        callback_data=f"{yt.video_id} vc {chat_id}")])
    else:
        audio_file_size = get_only_filesize(user_message_text)
        kb.append(
            [InlineKeyboardButton(f"دانلود صدا ({audio_file_size} mb)", callback_data=f"{yt.video_id} vc {chat_id}")])
    reply_markup = InlineKeyboardMarkup(kb)
    response = persian.select_quality if user_lang == "fa" else english.select_quality
    await update.message.reply_text(response, reply_markup=reply_markup, quote=True)
    await message_info.delete()
    users_collection.update_one(
        {"user_id": user.id},
        {"$set": {"last_download_time": time.time()}},
        upsert=True
    )


async def youtube_shorts_handler(update, context) -> None:
    user = update.effective_user
    chat_id = update.effective_chat.id
    user_message_text = update.message.text
    user_lang = users_collection.find_one({"user_id": user.id})["settings"]["language"]
    geting_info_response = persian.get_video_info if user_lang == "fa" else english.get_video_info
    message_info = await update.message.reply_text(geting_info_response, quote=True)
    kb = []
    yt = YouTube(user_message_text)
    try:
        video_options = get_video_options(yt)
    except AgeRestrictedError:
        response = persian.age_restricted if user_lang == "fa" else english.age_restricted
        await update.message.reply_text(response, quote=True)
        return
    for item in sorted(video_options, reverse=True):
        parts = item.split()
        if len(parts) == 2:
            quality, size = parts
            kb.append([InlineKeyboardButton(f"{quality} {size}",
                                            callback_data=f"{yt.video_id} {quality} {chat_id}")])
    reply_markup = InlineKeyboardMarkup(kb)
    response = persian.select_quality if user_lang == "fa" else english.select_quality
    await update.message.reply_text(response, reply_markup=reply_markup, quote=True)
    await message_info.delete()
