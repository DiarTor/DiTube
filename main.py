import logging
import os
import time

from config import API_ID, API_HASH, VIDEO_DOWNLOAD_DIR, BOT_TOKEN
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pytube import YouTube

# region bot config
bot = Client(
    "MiTube",
    bot_token=BOT_TOKEN,
    api_hash=API_HASH,
    api_id=API_ID
)
# endregion
# region log Configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# endregion
# region Database
# endregion
class BadLink(Exception):
    pass


# The Class that handles all the commands for downloading videos and sharing them with the user.
class Download:
    def __init__(self, bot):
        self.bot = bot

    def get_resolution_options(self, yt):
        resolution_options = []
        for res in yt.streams.filter(progressive=True).order_by("resolution"):
            if res is not None:
                resolution_options.append(res.resolution)
        return resolution_options

    def download_video(self, yt, quality):
        video = yt.streams.filter(resolution=quality, progressive=True).first()
        if video is not None:
            video_title = yt.title
            if "|" in video_title:
                video_title = video_title.replace("|", " ")
            video_path = os.path.join(VIDEO_DOWNLOAD_DIR, f"{video_title}.mp4")
            video.download(output_path=VIDEO_DOWNLOAD_DIR, filename=f"{video_title}.mp4")
            return video_path
        else:
            raise Exception("Selected quality not available for download")

    def send_video(self, yt, chat_id, video_path):
        channel_url = yt.channel_url
        views = yt.views
        description = yt.description[:950] if yt.description else ""
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Creator YT Channel", url=channel_url)]
        ])
        self.bot.send_video(
            chat_id=chat_id,
            video=video_path,
            caption=f"*{yt.title}*\n\n👀 Views: {views}\n\n📝 Description: {description}",
            reply_markup=keyboard
        )

    def process_video(self, link, quality, chat_id):
        try:
            yt = YouTube(link)
            video_path = self.download_video(yt, quality)
            self.send_video(yt, chat_id, video_path)
            os.remove(video_path)  # Remove the downloaded video after sending
        except Exception as e:
            logger.error(f"Error processing video: {e}")


# The Funtion That Greets the user and starts the bot.
@bot.on_message(filters.command("start"))
def greeting(bot, msg: Message):
    msg.reply("Hi And Welcome 😊\nPlease Send Me Your Video URL")


# The Function that gets the video link from the user and selects the quality.
@bot.on_message(filters.text)
def main(bot, msg: Message):
    chat_id = msg.chat.id
    text = msg.text
    if text.startswith("https://youtu.be/"):
        try:
            bot_instance = Download(bot)
            yt = YouTube(text)
            video_title = yt.title
            kb = []
            resolution_options = bot_instance.get_resolution_options(yt)
            for k in sorted(list(set(resolution_options))):
                kb.append([InlineKeyboardButton(
                    f"{k}", callback_data=f"{text} {k} {chat_id}"
                )])
            reply_markup = InlineKeyboardMarkup(kb)
            msg.reply("❓Choose The Quality :", reply_markup=reply_markup, quote=True)
        except BadLink:
            msg.reply("❌ Bad link Please Try Again")
        except Exception as e:
            logger.error(f"Error fetching video info: {e}")
            time.sleep(10)  # Wait for 10 seconds before retrying


# The Function that sends the video to the class that handles all the commands for downloading videos
@bot.on_callback_query()
def download_chosen_quality(bot, call):
    link, res_code, chat_id = call.data.split(" ", 2)
    call.edit_message_text("✨Downloading...")
    try:
        bot_instance = Download(bot)
        bot_instance.process_video(link=link, quality=res_code, chat_id=chat_id)
        call.edit_message_text("✅ Here Is Your Video :")
    except http.client.IncompleteRead:
        call.edit_message_text("❌ Something is Wrong With Our Servers! Please Try Again.")
    except Exception as e:
        logger.error(f"Error processing download: {e}")


if __name__ == "__main__":
    bot.run()
