from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import Update


async def send(update: Update, yt, chat_id, video_path) -> None:
    channel_url = yt.channel_url
    views = yt.views
    description = yt.description[:950] if yt.description else ""
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Creator YT Channel", url=channel_url)]])
    await update.effective_chat.send_video(video=video_path,
                                           caption=f"{yt.title}\n👀 Views: {views}\n📝 Description:\n{description}",
                                           reply_markup=keyboard)
