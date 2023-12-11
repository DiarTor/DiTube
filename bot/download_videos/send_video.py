import telebot
from bot.user_management.utils.user_utils import UserManager
from languages import persian, english
from requests.exceptions import ConnectionError
from telebot.apihelper import ApiTelegramException
from bot.common.button_utils import KeyboardMarkupGenerator
from pytube import YouTube

def send_video(msg: telebot.types.Message, bot: telebot.TeleBot, link, chat_id, video_path, user_id, quality):
    yt = YouTube(link)
    kb = KeyboardMarkupGenerator(user_id)
    if video_path.endswith((".mp4", ".mp3")):
        user_manager = UserManager(user_id)
        keyboard = kb.post_caption_buttons(yt.channel_url, link)
        media_type = "video" if video_path.endswith(".mp4") else "audio"
        publish_date = yt.publish_date.strftime("%Y/%m/%d")
        description = yt.description[:850] if yt.description else ""
        thumbnail_url = yt.thumbnail_url
        if quality == "vc":
            quality = "320kbps"
        caption = user_manager.return_response_based_on_language(
            persian=persian.caption.format(yt.title, quality, yt.views, description, publish_date),
            english=english.caption.format(yt.title, quality, yt.views, description, publish_date))
    try:
        if media_type == "video":
            bot.send_video(chat_id=chat_id, video=open(video_path, "rb"), caption=caption, supports_streaming=True, thumbnail=thumbnail_url,
                           duration=yt.length,
                           reply_markup=keyboard, parse_mode="markdown")
        elif media_type == "audio":
            bot.send_audio(chat_id=chat_id, audio=open(video_path, "rb"), caption=caption, reply_markup=keyboard, parse_mode="markdown")
    except (ConnectionError, ApiTelegramException):
        if ConnectionError:
            response = user_manager.return_response_based_on_language(persian=persian.connection_error,
                                                                      english=english.connection_error)
            bot.send_message(chat_id=chat_id, text=response)
        elif ApiTelegramException:
            response = user_manager.return_response_based_on_language(persian=persian.cant_download_larger_than_50mb,
                                                                      english=english.cant_download_larger_than_50mb)
            bot.send_message(chat_id=chat_id, text=response)
