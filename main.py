from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pytube import YouTube
import logging
import http
import os
bot = Client(
    "MiTube", bot_token="#place your bot token", api_hash="place your api_hash", api_id=place your api id)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class BadLink(Exception):
    pass


def get_resolution(link):
    resolution = []
    link = link.streams.filter(progressive=True)
    for res in link.order_by("resolution"):
        if res is not None:
            resolution.append(res.resolution)
    return resolution


def download_video(link, quality):
    yt = YouTube(link)
    video = yt.streams.filter(
        resolution=quality, progressive=True).first()
    video_title = video.title
    if "|" in video_title:
        link.replace("|", " ")
    video.download(f"D:/Codes/MiTube/videos/", filename=f"{video_title}.mp4")


def send(link, chat_id):
    video = YouTube(link)
    video_title = video.title
    file = f"D:/Codes/MiTube/videos/{video_title}.mp4"
    channel_url = video.channel_url
    views = video.views
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Creator YT Channel", url=channel_url)
        ]
    ])
    try:
        description = video.description[0:950]
    except TypeError:
        description = video.description
    bot.send_video(chat_id=chat_id, video=file,
                   caption=f"*{video_title}*\n\n👀 Views : {views}\n\n📝 Description : {description}", reply_markup=keyboard)
    if os.path.exists(f"D:/Codes/MiTube/videos/{video_title}.mp4"):
        os.remove(f"D:/Codes/MiTube/videos/{video_title}.mp4")
    else:
        pass


@bot.on_message(filters.command("start"))
def greeting(bot, msg: Message):
    msg.reply("Hi And Welcome 😊\nPlease Send Me Your Video URL")


@bot.on_message(filters.text)
def main(bot, msg: Message):
    global video_title
    chat_id = msg.chat.id
    text = msg.text
    if text[0:17] in ("https://youtu.be/"):
        try:
            video = YouTube(text)
            video_title = video.title
            kb = []
            for k in sorted(list(set(get_resolution(video)))):
                kb.append([InlineKeyboardButton(
                    f"{k}", callback_data=f"{text} {k} {chat_id}"
                )])
            reply_markup = InlineKeyboardMarkup(kb)
            msg.reply("❓Choose The Quality :",
                      reply_markup=reply_markup, quote=True)
        except BadLink:
            msg.reply("❌ Bad link Please Try Again")
            if os.path.exists(f"D:/Codes/MiTube/videos/{video_title}.mp4"):
                os.remove(f"D:/Codes/MiTube/videos/{video_title}.mp4")
            else:
                pass
        else:
            pass


@bot.on_callback_query()
def download_choosen_quality(bot, call):
    link, res_code, chat_id = call.data.split(" ", 2)
    call.edit_message_text("✨Downlaoding...")
    try:
        download_video(link=link, quality=res_code)
        call.edit_message_text("📨Sending...")
        send(link=link, chat_id=chat_id)
        call.edit_message_text("✅ Here Is Your Video :")
    except http.client.IncompleteRead:
        call.edit_message_text(
            "❌ Somthing is Wrong With Our Servers! Please Try Again.")


bot.run()
