import telebot.types
from bot.download_videos.get_video_information import get_only_filesize
from bot.download_videos.process_video import process_video
from bot.handlers.start_handler import StartCommandHandler
from bot.user_management.subscription.apps.buy_subscription import BuySubscription
from bot.user_management.utils.subscription_utils import SubscriptionManager
from bot.user_management.utils.user_utils import UserManager
from config.database import users_collection
from languages import persian, english


class CallbackHandler:
    def send_error_message(self, error_message):
        self.bot.answer_callback_query(self.callback.id, error_message, show_alert=True)

    def check_subscription_limit(self, filesize):
        subscription_manager = SubscriptionManager(self.callback.from_user.id, filesize)
        if subscription_manager.is_file_size_exceeded() or subscription_manager.is_daily_data_exceeded():
            if subscription_manager.is_file_size_exceeded():
                response = self.user_manager.return_response_based_on_language(persian=persian.file_data_exceeded,
                                                                               english=english.file_data_exceeded)
            elif subscription_manager.is_daily_data_exceeded():
                response = self.user_manager.return_response_based_on_language(persian=persian.daily_limit_exceeded,
                                                                               english=english.daily_limit_exceeded)
            self.send_error_message(response)
            return True
        return False

    def process_callback(self, callback: telebot.types.CallbackQuery, bot: telebot.TeleBot):
        self.callback = callback
        self.bot = bot
        the_user = users_collection.find_one({"user_id": callback.from_user.id})
        self.user_manager = UserManager(callback.from_user.id)
        user_lang = the_user["settings"]["language"]
        data = callback.data
        self.chat_id = callback.message.chat.id
        if data not in {"invite_referrals", "charge_account", "auto_renew", "check_joined", "premium_30_in_list",
                        "premium_60_in_list", "account_charge", "back_to_subscriptions_list",
                        "buy_premium_30_direct_payment", "buy_premium_30_account_charge",
                        "buy_premium_60_account_charge", "buy_premium_60_direct_payment"}:
            video_id, res_code_or_vc, chat_id = data.split(" ", 2)
            link = f"https://www.youtube.com/watch?v={video_id}"
            filesize = get_only_filesize(link, res_code_or_vc) if res_code_or_vc != "vc" else get_only_filesize(link)

            if not res_code_or_vc == "vc":
                if res_code_or_vc == "1080p" and the_user['subscription']['type'] == "bronze":
                    response = self.user_manager.return_response_based_on_language(persian=persian.cant_download_1080p,
                                                                                   english=english.cant_download_1080p)
                    self.send_error_message(response)
                    return

            if self.check_subscription_limit(filesize):
                return

            processing_message = self.user_manager.return_response_based_on_language(persian=persian.processing_message,
                                                                                     english=english.processing_message)
            self.bot.edit_message_text(processing_message, self.chat_id, message_id=self.callback.message.id)

            process_video(msg=telebot.types.Message, bot=self.bot, link=link, quality_or_audio=res_code_or_vc,
                          chat_id=self.chat_id, user_id=self.callback.from_user.id)

            self.bot.delete_message(chat_id=self.chat_id, message_id=self.callback.message.message_id)
            SubscriptionManager(self.callback.from_user.id, filesize).change_user_subscription_data()

        elif data == "invite_referrals":
            referral_banner = self.user_manager.return_response_based_on_language(
                persian=persian.invite_referral_banner, english=english.invite_referral_banner)
            referral_link = f'https://t.me/DitubeBot?start=ref_{self.callback.from_user.id}'
            self.bot.send_message(self.chat_id, referral_banner.format(referral_link))
            self.bot.send_message(self.chat_id, self.user_manager.return_response_based_on_language(
                persian=persian.invite_referral_guide, english=english.invite_referral_guide))

        elif data == "check_joined":
            if self.user_manager.is_subscribed_to_channel(callback, bot):
                StartCommandHandler().process_start_command(callback.message, bot)
                bot.delete_message(chat_id=self.chat_id, message_id=self.callback.message.message_id)
            else:
                response = self.user_manager.return_response_based_on_language(
                    persian=persian.not_subscribed_to_channel, english=english.not_subscribed_to_channel)
                self.bot.answer_callback_query(self.callback.id, response, show_alert=True)
        elif data == "premium_30_in_list":
            BuySubscription().show_subscription_details(msg=self.callback.message, bot=self.bot,
                                                        subscription="premium_30", user_id=self.callback.from_user.id)
        elif data == "premium_60_in_list":
            BuySubscription().show_subscription_details(msg=self.callback.message, bot=self.bot,
                                                        subscription="premium_60", user_id=self.callback.from_user.id)
        elif data in {"buy_premium_30_account_charge", "buy_premium_60_account_charge"}:
            BuySubscription().buy_via_account_charge(msg=self.callback.message, bot=self.bot, subscription=data, user_id=self.callback.from_user.id)
        elif data == "back_to_subscriptions_list":
            BuySubscription().return_to_subscriptions_list(msg=self.callback.message, bot=self.bot, user_id=self.callback.from_user.id)
        elif data in {"charge_account", "auto_renew", "buy_premium_30_direct_payment", "buy_premium_60_direct_payment"}:
            response = self.user_manager.return_response_based_on_language(persian=persian.coming_soon,
                                                                           english=english.coming_soon)
            self.bot.answer_callback_query(self.callback.id, response)
