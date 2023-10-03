from bot.database import users_collection
from bot.download_videos.process_video import process
from telegram import Update
from telegram.ext import CallbackContext
from bot.download_videos.get_video_information import get_only_filesize
from utils.check_download_limit import file_size_exceeded, monthly_file_size_exceeded
from telegram.error import TimedOut
from utils.user_database_data import change_user_subscription_size
async def handle_callback(update: Update, context: CallbackContext):
    the_user = users_collection.find_one({"user_id": update.effective_user.id})
    user_lang = the_user["settings"]["language"]
    query = update.callback_query
    data = query.data
    link, res_code_or_vc, chat_id= data.split(" ", 2)
    if not res_code_or_vc == "vc":
        filesize = get_only_filesize(link, res_code_or_vc)
        if not file_size_exceeded(user_data=the_user, file_size=filesize):
            await query.edit_message_text("❌File Size Exceeded.")
            return
        elif not monthly_file_size_exceeded(user_data=the_user, file_size=filesize):
            await query.edit_message_text("❌Monthly Size Exceeded.")
            return
    elif res_code_or_vc == "vc":
        filesize = get_only_filesize(link)
        if not file_size_exceeded(user_data=the_user, file_size=filesize):
            await query.edit_message_text("❌File Size Exceeded.")
            return
    if not link.startswith("https://youtu.be/"):
        link = f"https://youtube.com/shorts/{link}"
    if user_lang == "en":
        await query.edit_message_text("✨Processing...")
    else:
        await query.edit_message_text("✨درحال پردازش...")
    try:
        await process(update=update, link=link, quality_or_audio=res_code_or_vc, chat_id=chat_id)
        await change_user_subscription_size(user=the_user, filesize=filesize)

    except TimedOut :
        await query.edit_message_text("❌Time Out, Dont worry no size has been used from your subscription, please try again")
    await query.delete_message()
