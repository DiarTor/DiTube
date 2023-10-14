from bot.database import users_collection
from bot.download_videos.get_video_information import get_only_filesize
from bot.download_videos.process_video import process
from telegram import Update
from telegram.error import TimedOut
from telegram.ext import CallbackContext
from utils.check_download_limit import file_size_exceeded, daily_file_size_exceeded
from utils.modify_user_data import change_user_subscription_size


async def handle_callback(update: Update, context: CallbackContext):
    the_user = users_collection.find_one({"user_id": update.effective_user.id})
    user_lang = the_user["settings"]["language"]
    query = update.callback_query
    data = query.data
    video_id, res_code_or_vc, chat_id = data.split(" ", 2)
    if not res_code_or_vc == "vc":
        if res_code_or_vc == "1080p" and the_user['subscription']['type'] == "bronze":
            await query.edit_message_text(
                "❌You cant download 1080p ! To gain access to this quality please buy a subscription.")
            return
        link = f"https://www.youtube.com/watch?v={video_id}"
        filesize = get_only_filesize(link, res_code_or_vc)
        if not file_size_exceeded(user_data=the_user, file_size=filesize):
            await query.edit_message_text("❌File Data Exceeded.")
            return
        elif not daily_file_size_exceeded(user_data=the_user, file_size=filesize):
            await query.edit_message_text("❌Daily Data Exceeded.")
            return
    elif res_code_or_vc == "vc":
        link = f"https://www.youtube.com/watch?v={video_id}"
        filesize = get_only_filesize(link)
        if not file_size_exceeded(user_data=the_user, file_size=filesize):
            await query.edit_message_text("❌File Data Exceeded.")
            return
        elif not daily_file_size_exceeded(user_data=the_user, file_size=filesize):
            await query.edit_message_text("❌Daily Data Exceeded.")
            return
    if user_lang == "en":
        await query.edit_message_text("✨Processing...")
    else:
        await query.edit_message_text("✨درحال پردازش...")
    try:
        await process(update=update, link=link, quality_or_audio=res_code_or_vc, chat_id=chat_id)
        await change_user_subscription_size(user=the_user, filesize=filesize)

    except TimedOut:
        await query.edit_message_text(
            "❌Time Out, Dont worry no data has been used from your subscription, please try again.")
    await query.delete_message()
