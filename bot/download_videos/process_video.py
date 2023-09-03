import os

from pytube import YouTube
from telegram import Update
from telegram.error import TimedOut

from bot.database import users_collection
from bot.download_videos.download_video import download
from bot.download_videos.send_video import send
from langs import persian, english


async def process(update: Update, link, quality, chat_id):
    user_lang = users_collection.find_one({"user_id": update.effective_user.id})["lang"]
    try:
        yt = YouTube(link)
        video_path = download(yt, quality)
        await send(update=update, yt=yt, chat_id=chat_id, video_path=video_path)
        os.remove(video_path)
    except TimedOut:
        response = english.timed_out if user_lang == "en" else persian.timed_out
        await update.effective_chat.send_message(response)
