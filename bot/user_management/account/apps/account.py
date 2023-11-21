import datetime

import telebot.types
from bot.user_management.utils.button_utils import KeyboardMarkupGenerator
from bot.user_management.utils.user_utils import UserManager
from config.database import users_collection
from jdatetime import datetime as jdatetime
from languages import persian, english


def show_account_details(msg: telebot.types.Message, bot: telebot.TeleBot):
    user = msg.from_user
    usermanager = UserManager(user.id)
    user_lang = usermanager.get_user_language()
    format_number_with_commas = lambda number: f"{number:,}"
    user_register_date = users_collection.find_one({"user_id": user.id})["registered_at"]
    user_total_downloads = len(users_collection.find_one({"user_id": user.id})["downloads"])
    user_total_downloads_size = sum(i.get("size", 0) for i in
                                    users_collection.find_one({"user_id": user.id}).get("downloads",
                                                                                        [])) if users_collection.find_one(
        {"user_id": user.id}) else 0
    formated_user_total_downloads_size = "{:.1f}".format(user_total_downloads_size)
    formatted_balance = format_number_with_commas(users_collection.find_one({"user_id": user.id})["balance"])
    user_referrals = len(users_collection.find_one({"user_id": user.id})["referrals"])
    jalali_start_date = jdatetime.fromgregorian(
        datetime=datetime.datetime.strptime(user_register_date, "%Y-%m-%d %H:%M:%S"))
    user_jdate_register_date = jalali_start_date.strftime("%Y/%m/%d")
    buttons = KeyboardMarkupGenerator(user_id=user.id).account_buttons()
    response = usermanager.return_response_based_on_language(persian=persian.account_details.format(user.id,
                                                                                                    user_jdate_register_date,
                                                                                                    user_total_downloads,
                                                                                                    formated_user_total_downloads_size,
                                                                                                    formatted_balance,
                                                                                                    user_referrals),
                                                             english=english.account_details.format(user.id,
                                                                                                    user_register_date,
                                                                                                    user_total_downloads,
                                                                                                    formated_user_total_downloads_size,
                                                                                                    formatted_balance,
                                                                                                    user_referrals))

    bot.send_message(chat_id=msg.chat.id, text=response,
                     reply_markup=KeyboardMarkupGenerator(user.id).account_buttons(),
                     parse_mode="markdown")
