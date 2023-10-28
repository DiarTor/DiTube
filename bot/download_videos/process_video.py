import datetime
import os

import telebot.types
from bot.database import users_collection
from bot.download_videos.download_video import download_yt_video
from bot.download_videos.get_video_information import get_only_filesize
from bot.download_videos.send_video import send
from langs import persian, english
from pytube import YouTube
from telegram.error import TimedOut
from utils.get_user_data import get_user_lang

def process(msg: telebot.types.Message, bot: telebot.TeleBot, link, quality_or_audio, chat_id, user_id):
    user_lang = get_user_lang(user_id)
    try:
        yt = YouTube(link)
        video_path = download_yt_video(yt, quality_or_audio)
        send(msg=msg, bot=bot, yt=yt, chat_id=chat_id, video_path=video_path, user_id=user_id)
        os.remove(video_path)
        if quality_or_audio != "vc":
            res_code = quality_or_audio
        else:
            res_code = None
        download_entry = {
            "media_title": yt.title,
            "media_link": link,
            "video_audio": quality_or_audio,
            "duration": yt.length,
            "size": get_only_filesize(link, res_code),
            "creator_channel": yt.channel_url,
            "user_subscription": users_collection.find_one({"user_id": user_id})["subscription"][
                'type'],
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        users_collection.update_one({"user_id": user_id}, {"$push": {"downloads": download_entry}})
    except TimedOut:
        response = english.timed_out if user_lang == "en" else persian.timed_out
        bot.reply_to(response)
