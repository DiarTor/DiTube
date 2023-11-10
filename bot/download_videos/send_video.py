import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.get_user_data import get_user_lang
from requests.exceptions import ConnectionError

def send(msg: telebot.types.Message, bot: telebot.TeleBot, yt, chat_id, video_path, user_id):
    user_lang = get_user_lang(user_id)

    if video_path.endswith((".mp4", ".mp3")):
        creator_yt_channel_lang = "Creator YouTube Channel" if user_lang == "en" else "کانال یوتیوب سازنده"
        keyboard = InlineKeyboardMarkup().row(InlineKeyboardButton(creator_yt_channel_lang, url=yt.channel_url))
        media_type = "video" if video_path.endswith(".mp4") else "audio"
        caption = generate_caption(yt, user_lang)
    try:
        if user_lang == "en":
            if media_type == "video":
                bot.send_video(chat_id=chat_id, video=open(video_path, "rb"), caption=caption, reply_markup=keyboard)
            elif media_type == "audio":
                bot.send_audio(chat_id=chat_id, audio=open(video_path, "rb"), caption=caption, reply_markup=keyboard)
        elif user_lang == "fa":
            if media_type == "video":
                bot.send_video(chat_id=chat_id, video=open(video_path, "rb"), caption=caption, reply_markup=keyboard)
            elif media_type == "audio":
                bot.send_audio(chat_id=chat_id, audio=open(video_path, "rb"), caption=caption, reply_markup=keyboard)
    except ConnectionError:
        if user_lang == "en":
            bot.send_message(chat_id=chat_id, text="Connection Error")
        elif user_lang == "fa":
            bot.send_message(chat_id=chat_id, text="خطا در ارتباط با سرور")


def generate_caption(yt, user_lang):
    channel_url = yt.channel_url
    views = yt.views
    description = yt.description[:850] if yt.description else ""
    published = yt.publish_date.strftime("%Y/%m/%d")
    if user_lang == "en":
        caption = f"{yt.title}\n\n👀 Views: {views}\n\n📝 Description:\n{description}\n\n📅 Publish Date: {published} \n\n@DiTubebot"
        return caption
    elif user_lang == "fa":
        caption = f"{yt.title}\n\n👀 بازدید: {views}\n📝 توضیحات:\n{description}\n\n📅 تاریخ انتشار: {published} \n\n@DiTubebot"
        return caption
