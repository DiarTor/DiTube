import os

from pytube import YouTube
from telegram import Update

from bot.download.download_video import download
from bot.download.send_video import send


async def process(update: Update, link, quality, chat_id):
    try:
        yt = YouTube(link)
        video_path = download(yt, quality)
        await send(update=update, yt=yt, chat_id=chat_id, video_path=video_path)
        os.remove(video_path)
    except Exception as e:
        print(e)
