import telebot.types
from bot.download_videos.get_video_information import get_only_filesize
from bot.download_videos.process_video import process
from bot.user_management.utils.subscription_utils import SubscriptionManager
from bot.user_management.utils.user_utils import UserManager
from config.database import users_collection
from languages import persian
from bot.handlers.start_handler import StartCommandHandler
class CallbackHandler:
    def send_error_message(self, error_message):
        self.bot.answer_callback_query(self.callback.id, error_message, show_alert=True)

    def check_subscription(self, filesize):
        subscription_manager = SubscriptionManager(self.callback.from_user.id, filesize)
        if subscription_manager.is_file_size_exceeded() or subscription_manager.is_daily_data_exceeded():
            self.send_error_message(
                "❌File Data Exceeded." if not subscription_manager.is_daily_data_exceeded() else "❌Daily Data Exceeded.")
            return True
        return False

    def process_callback(self, callback: telebot.types.CallbackQuery, bot: telebot.TeleBot):
        self.callback = callback
        self.bot = bot
        the_user = users_collection.find_one({"user_id": callback.from_user.id})
        user_manager = UserManager(callback.from_user.id)
        user_lang = the_user["settings"]["language"]
        data = callback.data
        self.chat_id = callback.message.chat.id
        if data not in {"invite_referrals", "charge_account", "auto_renew", "check_joined"}:
            video_id, res_code_or_vc, chat_id = data.split(" ", 2)
            link = f"https://www.youtube.com/watch?v={video_id}"
            filesize = get_only_filesize(link, res_code_or_vc) if res_code_or_vc != "vc" else get_only_filesize(link)

            if not res_code_or_vc == "vc":
                if res_code_or_vc == "1080p" and the_user['subscription']['type'] == "bronze":
                    self.send_error_message(
                        "❌You can't download 1080p! To gain access to this quality, please buy a subscription.")
                    return

            if self.check_subscription(filesize):
                return

            processing_message = "✨Processing..." if user_lang == "en" else "✨درحال پردازش..."
            self.bot.edit_message_text(processing_message, self.chat_id, message_id=self.callback.message.id)

            process(msg=telebot.types.Message, bot=self.bot, link=link, quality_or_audio=res_code_or_vc,
                    chat_id=self.chat_id, user_id=self.callback.from_user.id)

            self.bot.delete_message(chat_id=self.chat_id, message_id=self.callback.message.message_id)
            SubscriptionManager(self.callback.from_user.id, filesize).change_user_subscription_data()

        elif data == "invite_referrals":
            referral_banner = user_manager.return_response_based_on_language(
                persian=persian.invite_referral_banner)
            referral_link = f'https://t.me/DitubeBot?start=ref_{self.callback.from_user.id}'
            self.bot.send_message(self.chat_id, referral_banner.format(referral_link))
            self.bot.send_message(self.chat_id, user_manager.return_response_based_on_language(
                persian=persian.invite_referral_guide))

        elif data == "check_joined":
            if user_manager.is_subscribed_to_channel(callback, bot):
                StartCommandHandler().process_start_command(callback.message, bot)
                bot.delete_message(chat_id=self.chat_id, message_id=self.callback.message.message_id)
            else:
                self.bot.answer_callback_query(self.callback.id, "You are not subscribed to this channel.")
        elif data in {"charge_account", "auto_renew"}:
            self.bot.answer_callback_query(self.callback.id, "⚡️Coming Soon...")
