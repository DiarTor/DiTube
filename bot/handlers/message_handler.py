import re

import telebot.types
from bot.handlers.yt_link_handler import YouTubeVideoHandler
from bot.user_management.account.apps.account import show_account_details
from bot.user_management.giftcode.apps.giftcode import redeem_giftcode
from bot.user_management.guide.apps.guide import send_guide_message
from bot.user_management.my_subscription.apps.my_subscription import show_user_subscription_details
from bot.user_management.settings.apps.language import join_in_selecting_lang
from bot.user_management.settings.apps.language import selected_lang_is_en, selected_lang_is_fa
from bot.user_management.settings.apps.settings import join_in_settings
from bot.user_management.support.apps.support import join_in_support, send_user_msg_to_support, \
    send_user_photo_to_support, \
    reply_to_user_support_msg
from bot.user_management.utils.button_utils import KeyboardMarkupGenerator
from bot.user_management.utils.user_utils import UserManager
from config.database import users_collection
from languages import persian, english


class MessageHandler:
    def __init__(self):
        """
        Initialize the MessageHandler class
        """
        self.support_group_id = -4043182903

    def handle_message(self, msg: telebot.types.Message, bot: telebot.TeleBot):
        self.usermanager = UserManager(msg.from_user.id)
        self.msg = msg
        self.bot = bot
        self.chat_id = msg.chat.id
        self.user_message_text = msg.text
        self.keyboardgenerator = KeyboardMarkupGenerator(msg.from_user.id)
        self.the_user = users_collection.find_one({"user_id": msg.from_user.id})
        # Check if the user is subscribed to the channel
        if not self.usermanager.is_subscribed_to_channel(msg, bot):
            response = self.usermanager.return_response_based_on_language(persian=persian.subscribe_to_channel,
                                                                          english=english.subscribe_to_channel)
            bot.send_message(self.chat_id, response,
                             reply_markup=self.keyboardgenerator.subscribe_to_channel_buttons())
            return

        # Check if the user is new and requires a restart
        if not users_collection.find_one({"user_id": msg.from_user.id}):
            bot.reply_to(msg, f"{persian.restart_required}\n\n{english.restart_required}")

        if self.the_user['settings']['language'] == 'not_selected' and self.user_message_text not in {'🇮🇷فارسی',
                                                                                                      '🇺🇸English'}:
            join_in_selecting_lang(msg, bot)
            return

        # Check if the message is a reply in the support group
        if self.chat_id == self.support_group_id and msg.reply_to_message:
            reply_to_user_support_msg(msg, bot)
            return

        # Check for YouTube video links
        if any(re.search(pattern, self.user_message_text) for pattern in [
            r'https://youtu.be/',
            r'https://www.youtube.com/watch\?v=',
            r'https://www.youtube.com/shorts/',
            r'https://youtube.com/shorts/',
            r'http://youtu.be/',
            r'http://www.youtube.com/watch\?v=',
            r'http://www.youtube.com/shorts/',
            r'http://youtube.com/shorts/'
        ]):
            YouTubeVideoHandler().process_video(msg, bot)
            return

        # Handle specific commands
        command_handlers = {
            "↩️ Return": self.handle_return,
            "🛒 Buy Subscription": self.handle_buy_subscription,
            "👤 Account": self.handle_account,
            "📋 My Subscription": self.handle_subscription,
            "🎁 Gift Code": self.handle_gift_code,
            "📖 Guide": self.handle_guide,
            "⚙️ Settings": self.handle_settings,
            "📞 Support": self.handle_support,
            "↩️ بازگشت": self.handle_return,
            "🛒 خرید اشتراک": self.handle_buy_subscription,
            "👤 حساب کاربری": self.handle_account,
            "📋 اشتراک من": self.handle_subscription,
            "🎁 کد هدیه": self.handle_gift_code,
            "📖 راهنما": self.handle_guide,
            "⚙️ تنظیمات": self.handle_settings,
            "📞 پشتیبانی": self.handle_support
        }

        # Check if the message corresponds to a known command
        if self.user_message_text in command_handlers:
            command_handlers[self.user_message_text]()
            return

        # Check for other conditions
        if self.the_user['metadata']["redeeming_code"]:
            redeem_giftcode(msg, bot)
        elif self.the_user['metadata']["joined_in_settings"]:
            self.handle_joined_settings()
        elif self.the_user['metadata']["selecting_language"]:
            self.handle_selecting_language()
        elif self.the_user['metadata']["joined_in_support"]:
            send_user_msg_to_support(msg, bot)
        elif self.usermanager.get_user_language() == "not_selected":
            self.the_user['metadata']["selecting_language"] = True
            bot.reply_to(msg, f"{persian.restart_required}\n\n{english.restart}")
        else:
            if not self.the_user['settings']['language'] == 'not_selected':
                response = self.usermanager.return_response_based_on_language(persian=persian.unknown_request,
                                                                              english=english.unknown_request)
                bot.reply_to(msg, response)

    def handle_return(self):
        # Handle the "Return" command
        response = self.usermanager.return_response_based_on_language(persian=persian.returned_to_homepage,
                                                                      english=english.returned_to_homepage)
        self.bot.send_message(self.chat_id, response, reply_markup=self.keyboardgenerator.homepage_buttons())
        for field in ["selecting_language", "joined_in_settings", "redeeming_code", "joined_in_support"]:
            users_collection.update_one({"_id": self.the_user["_id"]}, {"$set": {"metadata." + field: False}})

    def handle_buy_subscription(self):
        # Handle the "Buy Subscription" Button
        response = self.usermanager.return_response_based_on_language(
            persian=persian.buy_subscription_currently_not_available,
            english=english.buy_subscription_currently_not_available)
        self.bot.reply_to(self.msg, response)

    def handle_account(self):
        # Handle the "Account" Button
        show_account_details(self.msg, self.bot)

    def handle_subscription(self):
        # Handle the "My Subscription" Button
        show_user_subscription_details(self.msg, self.bot)

    def handle_gift_code(self):
        # Handle the "Gift Code" Button
        response = self.usermanager.return_response_based_on_language(persian=persian.send_the_giftcode,
                                                                      english=english.send_the_giftcode)
        self.bot.send_message(self.chat_id, response, reply_markup=self.keyboardgenerator.return_buttons())
        users_collection.update_one(filter={"_id": self.the_user["_id"]},
                                    update={"$set": {"metadata.redeeming_code": True}})

    def handle_guide(self):
        # Handle the "Guide" Button
        send_guide_message(self.msg, self.bot)

    def handle_settings(self):
        # Handle the "Settings" Button
        join_in_settings(self.msg, self.bot)

    def handle_support(self):
        # Handle the "Support" Button
        join_in_support(self.msg, self.bot)

    def handle_joined_settings(self):
        # Handle when the user has joined settings
        if self.user_message_text == "🌐 Change Language" or self.user_message_text == "🌐 تغییر زبان":
            join_in_selecting_lang(self.msg, self.bot)
            users_collection.update_one(filter={"_id": self.the_user["_id"]},
                                        update={"$set": {"metadata.joined_in_settings": False}})
        else:
            response = self.usermanager.return_response_based_on_language(persian=persian.unknown_request,
                                                                          english=english.unknown_request)
            self.bot.reply_to(self.msg, self.response)

    def handle_selecting_language(self):
        # Handle when the user is selecting a language
        if self.user_message_text == "🇮🇷فارسی":
            selected_lang_is_fa(self.msg, self.bot)
        elif self.user_message_text == "🇺🇸English":
            selected_lang_is_en(self.msg, self.bot)

    def handle_photo(self, msg: telebot.types.Message, bot: telebot.TeleBot):
        the_user = users_collection.find_one({"user_id": msg.from_user.id})
        if msg.chat.id == self.support_group_id and msg.reply_to_message:
            reply_to_user_support_msg(msg, bot)
        if the_user['metadata']["joined_in_support"] == True:
            send_user_photo_to_support(msg, bot)
