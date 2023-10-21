from bot.database import users_collection
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import Update


async def send(update: Update, yt, chat_id, video_path) -> None:
    user_lang = users_collection.find_one({"user_id": update.effective_user.id})["settings"]["language"]
    channel_url = yt.channel_url
    views = yt.views
    description = yt.description[:850] if yt.description else ""
    published = yt.publish_date.strftime("%d/%m/%Y")
    if user_lang == "en":
        if "mp4" in video_path:
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Creator YT Channel", url=channel_url)]])
            await update.effective_chat.send_video(video=video_path,
                                                   caption=f"{yt.title}\n\n👀 Views: {views}\n📝 Description:\n{description}\n\n📅 Publish Date: {published}",
                                                   reply_markup=keyboard)
        else:
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Creator YT Channel", url=channel_url)]])
            await update.effective_chat.send_audio(audio=video_path,
                                                   caption=f"{yt.title}\n\n👀 Views: {views}\n📝 Description:\n{description}\n\n📅 Publish Date: {published}",
                                                   reply_markup=keyboard)
    else:
        if "mp4" in video_path:
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Creator YT Channel", url=channel_url)]])
            await update.effective_chat.send_video(video=video_path,
                                                   caption=f"{yt.title}\n\n👀 Views: {views}\n📝 Description:\n{description}\n\n📅 Publish Date: {published}",
                                                   reply_markup=keyboard)
        else:
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Creator YT Channel", url=channel_url)]])
            await update.effective_chat.send_audio(audio=video_path,
                                                   caption=f"{yt.title}\n\n👀 Views: {views}\n📝 Description:\n{description}\n\n📅 Publish Date: {published}",
                                                   reply_markup=keyboard)
