import datetime

import telebot.types
from bot.user_management.account.apps.referral import referral_handler
from bot.user_management.account.apps.settings.language import join_in_selecting_lang
from bot.user_management.utils.button_utils import KeyboardMarkupGenerator
from bot.user_management.utils.user_utils import UserManager
from config.database import users_collection
from languages import persian, english


class StartCommandHandler:
    def create_default_user_data(self, msg: telebot.types.Message):
        """
        Create default user data if the user is new.

        This function creates default user data if the user is not found in the database.
        """
        if not users_collection.find_one({"user_id": msg.from_user.id}):
            user = msg.from_user
            user_data = {
                "user_id": user.id,
                "user_name": user.username,
                "user_firstname": user.first_name,
                "user_lastname": user.last_name,
                "balance": 0,
                "referrals": [],
                "referral_total_profit": 0,
                "referraled": None,
                "registered_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "subscription": {
                    "type": "free",
                    "max_file_size": 200,
                    "max_data_per_day": 500,
                    "used_data": 0,
                    "remaining_data": 800,
                    "last_reset_date": datetime.date.today().strftime("%Y-%m-%d"),
                },
                "downloads": [],
                "settings": {
                    "language": "not_selected",
                },
                "metadata": {
                    "selecting_language": False,
                    "joined_in_settings": False,
                    "redeeming_code": False,
                    "joined_in_support": False

                },
            }
            users_collection.insert_one(user_data)
        self.the_user = users_collection.find_one({"user_id": msg.from_user.id})

    def update_metadata_flags(self):
        """
        Update metadata flags for various settings.

        This function updates metadata flags for language selection, settings joining, redeeming code, and support joining.
        """
        for field in ["selecting_language", "joined_in_settings", "redeeming_code", "joined_in_support"]:
            users_collection.update_one({"_id": self.the_user["_id"]}, {"$set": {"metadata." + field: False}})

    def process_start_command(self, msg: telebot.types.Message, bot: telebot.TeleBot):
        """
        Process the /start command.

        This function handles the entire process of processing the /start command.
        """
        self.create_default_user_data(msg=msg)
        self.update_metadata_flags()
        user_manager = UserManager(user_id=msg.from_user.id)

        args = msg.text.split()[1:]
        if args and self.the_user["settings"]["language"] == "not_selected":
            referral_handler(msg=msg, bot=bot, referral_user_id=args)

        if not user_manager.is_subscribed_to_channel(msg, bot):
            response = user_manager.return_response_based_on_language(persian=persian.subscribe_to_channel,
                                                                      english=english.subscribe_to_channel)
            bot.send_message(msg.chat.id, response,
                             reply_markup=KeyboardMarkupGenerator(msg.from_user.id).subscribe_to_channel_buttons())
            return

        if self.the_user["settings"]["language"] == "not_selected":
            join_in_selecting_lang(msg, bot)
        else:
            response = user_manager.return_response_based_on_language(persian=persian.greeting,
                                                                      english=english.greeting)
            bot.send_message(chat_id=msg.chat.id, text=response,
                             reply_markup=KeyboardMarkupGenerator(msg.from_user.id).homepage_buttons())
