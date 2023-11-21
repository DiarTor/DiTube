import telebot
from bot.user_management.utils.user_utils import UserManager
from languages import persian, english
from requests.exceptions import ConnectionError
from telebot.apihelper import ApiTelegramException
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def send(msg: telebot.types.Message, bot: telebot.TeleBot, yt, chat_id, video_path, user_id):
    if video_path.endswith((".mp4", ".mp3")):
        user_manager = UserManager(msg.from_user.id)
        keyboard = InlineKeyboardMarkup().row(InlineKeyboardButton(
            user_manager.return_response_based_on_language(persian=persian.creator_channel,
                                                           english=english.creator_channel), url=yt.channel_url))
        media_type = "video" if video_path.endswith(".mp4") else "audio"
        caption = user_manager.return_response_based_on_language(
            persian=persian.caption.format(yt.title, yt.views, yt.description[:850] if yt.description else "",
                                           yt.publish_date.strftime("%Y/%m/%d")),
            english=english.caption.format(yt.title, yt.views, yt.description[:850] if yt.description else "",
                                           yt.publish_date.strftime("%Y/%m/%d")))
    try:
        if media_type == "video":
            bot.send_video(chat_id=chat_id, video=open(video_path, "rb"), caption=caption, supports_streaming=True,
                           reply_markup=keyboard)
        elif media_type == "audio":
            bot.send_audio(chat_id=chat_id, audio=open(video_path, "rb"), caption=caption, reply_markup=keyboard)
    except (ConnectionError, ApiTelegramException):
        if ConnectionError:
            response = user_manager.return_response_based_on_language(persian=persian.connection_error,
                                                                      english=english.connection_error)
            bot.send_message(chat_id=chat_id, text=response)
        elif ApiTelegramException:
            response = user_manager.return_response_based_on_language(persian=persian.cant_download_larger_than_50mb,
                                                                      english=english.cant_download_larger_than_50mb)
            bot.send_message(chat_id=chat_id, text=response)
