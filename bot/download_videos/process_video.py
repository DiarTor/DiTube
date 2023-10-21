import os

from bot.database import users_collection
from bot.download_videos.download_video import download_yt_video
from bot.download_videos.send_video import send
from langs import persian, english
from pytube import YouTube
from telegram import Update
from telegram.error import TimedOut
import datetime
from bot.download_videos.get_video_information import get_only_filesize


async def process(update: Update, link, quality_or_audio, chat_id):
    user_lang = users_collection.find_one({"user_id": update.effective_user.id})["settings"]["language"]
    try:
        yt = YouTube(link)
        video_path = download_yt_video(yt, quality_or_audio)
        await send(update=update, yt=yt, chat_id=chat_id, video_path=video_path)
        os.remove(video_path)
        if quality_or_audio != "vc":
            res_code = quality_or_audio
        else:
            res_code = None
        download_entry = {
            "video_title": yt.title,
            "video_link": link,
            "quality_or_audio": quality_or_audio,
            "duration": yt.length,
            "size": get_only_filesize(link, res_code),
            "creator_channel": yt.channel_url,
            "user_subscription": users_collection.find_one({"user_id": update.effective_user.id})["subscription"]['type'],
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        users_collection.update_one({"user_id": update.effective_user.id}, {"$push": {"downloads": download_entry}})
    except TimedOut:
        response = english.timed_out if user_lang == "en" else persian.timed_out
        await update.effective_chat.send_message(response)
