import os

from bot.database import users_collection
from bot.download_videos.download_video import download_yt_video
from bot.download_videos.send_video import send
from langs import persian, english
from pytube import YouTube
from telegram import Update
from telegram.error import TimedOut


async def process(update: Update, link, quality_or_audio, chat_id):
    user_lang = users_collection.find_one({"user_id": update.effective_user.id})["settings"]["language"]
    try:
        yt = YouTube(link)
        video_path = download_yt_video(yt, quality_or_audio)
        await send(update=update, yt=yt, chat_id=chat_id, video_path=video_path)

        os.remove(video_path)
    except TimedOut:
        response = english.timed_out if user_lang == "en" else persian.timed_out
        await update.effective_chat.send_message(response)
