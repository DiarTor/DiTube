import datetime
import re

import telebot.types
from bot.user_management.settings.apps.language import join_in_selecting_lang
from bot.user_management.utils.button_utils import KeyboardMarkupGenerator
from bot.user_management.utils.user_utils import UserManager
from config.database import users_collection
from languages import persian


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
                "referraled": None,
                "registered_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "subscription": {
                    "type": "bronze",
                    "status": "active",
                    "price": 0,
                    "start_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "expire_date": None,
                    "auto_renew": False,
                    "max_file_size": 200,
                    "max_data_per_day": 800,
                    "used_data": 0,
                    "remaining_data": 800,
                    "last_reset_date": datetime.date.today().strftime("%Y-%m-%d"),
                    "history": [
                        {
                            "event_type": "subscription_created",
                            "subscription_type": "bronze",
                            "price": 0,
                            "subscription_date": "",
                            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "details": "User upgraded to free subscription",
                        }
                    ],
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

    def process_referral_code(self, msg: telebot.types.Message, args):
        """
        Process referral code if provided in the command arguments.

        :param args: Command arguments.
        """
        referral_code_match = re.match(r'ref_(\w+)', args[0])
        user_id = msg.from_user.id
        if referral_code_match:
            referral_code = int(referral_code_match.group(1))
            if self.the_user and not self.the_user.get("referraled"):
                referral_user = users_collection.find_one({"user_id": referral_code})
                if referral_user and user_id != referral_code and referral_code not in referral_user.get("referrals",
                                                                                                         []):
                    users_collection.update_one({"user_id": referral_code}, {"$push": {"referrals": user_id}})
                    users_collection.update_one({"user_id": user_id}, {"$set": {"referraled": referral_code}})
                else:
                    bot.reply_to(msg, "Invalid referral code")
            else:
                bot.reply_to(msg, "You've already used a referral code.")

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
            self.process_referral_code(args=args, msg=msg)

        if not user_manager.is_subscribed_to_channel(msg, bot):
            response = user_manager.return_response_based_on_language(persian=persian.subscribe_to_channel)
            bot.send_message(msg.chat.id, response,
                                  reply_markup=KeyboardMarkupGenerator(msg.from_user.id).subscribe_to_channel_buttons())
            return

        if self.the_user["settings"]["language"] == "not_selected":
            join_in_selecting_lang(msg, bot)
        else:
            response = user_manager.return_response_based_on_language(persian=persian.greeting)
            bot.send_message(chat_id=msg.chat.id, text=response,
                                  reply_markup=KeyboardMarkupGenerator(msg.from_user.id).homepage_buttons())
