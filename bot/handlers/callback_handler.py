import telebot.types
from bot.database import users_collection
from bot.download_videos.get_video_information import get_only_filesize
from bot.download_videos.process_video import process
from utils.check_download_limit import file_size_exceeded, daily_file_size_exceeded
from utils.modify_user_data import change_user_subscription_data


def handle_callback(callback: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    the_user = users_collection.find_one({"user_id": callback.from_user.id})
    user_lang = the_user["settings"]["language"]
    data = callback.data
    chat_id = callback.message.chat.id
    if data != "invite_referrals" and data != "charge_account" and data != "auto_renew":
        video_id, res_code_or_vc, chat_id = data.split(" ", 2)
        if not res_code_or_vc == "vc":
            if res_code_or_vc == "1080p" and the_user['subscription']['type'] == "bronze":
                bot.edit_message_text(
                    "❌You cant download 1080p ! To gain access to this quality please buy a subscription.", chat_id,
                    message_id=callback.message.id)
                return
            link = f"https://www.youtube.com/watch?v={video_id}"
            filesize = get_only_filesize(link, res_code_or_vc)
            if not file_size_exceeded(user_data=the_user, file_size=filesize):
                bot.edit_message_text("❌File Data Exceeded.", chat_id, message_id=callback.message.id)
                return
            elif not daily_file_size_exceeded(user_data=the_user, file_size=filesize):
                bot.edit_message_text("❌Daily Data Exceeded.", chat_id, message_id=callback.message.id)
                return
        elif res_code_or_vc == "vc":
            link = f"https://www.youtube.com/watch?v={video_id}"
            filesize = get_only_filesize(link)
            if not file_size_exceeded(user_data=the_user, file_size=filesize):
                bot.edit_message_text("❌File Data Exceeded.", chat_id, message_id=callback.message.id)
                return
            elif not daily_file_size_exceeded(user_data=the_user, file_size=filesize):
                bot.edit_message_text("❌Daily Data Exceeded.", chat_id, message_id=callback.message.id)
                return
        if user_lang == "en":
            bot.edit_message_text("✨Processing...", chat_id, message_id=callback.message.id)
        else:
            bot.edit_message_text("✨درحال پردازش...", chat_id, message_id=callback.message.id)

        process(msg=telebot.types.Message, bot=bot, link=link, quality_or_audio=res_code_or_vc, chat_id=chat_id,
                user_id=callback.from_user.id)
        change_user_subscription_data(user=the_user, filesize=filesize)

        bot.delete_message(chat_id=chat_id, message_id=callback.message.message_id)

    elif data == "invite_referrals":
        bot.send_message(callback.message.chat.id,
                         f"Share this link to your friends.\nhttps://t.me/DiarTorBot?start=ref_{callback.from_user.id}")
    elif data == "charge_account":
        bot.answer_callback_query(callback.id, "⚡️Coming Soon...")
    elif data == "auto_renew":
        bot.answer_callback_query(callback.id, "⚡️Coming Soon...")
