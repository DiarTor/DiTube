import telebot.types
from bot.user_management.utils.user_utils import UserManager
from languages import persian, english


def show_user_subscription_details(msg: telebot.types.Message, bot: telebot.TeleBot):
    user_manager = UserManager(msg.from_user.id)
    subscription_data = user_manager.get_user_subscription_details()
    used_data = subscription_data['used_data']
    remaining_data = subscription_data['remaining_data']
    formatted_used_data = "{:.1f}".format(used_data)
    formatted_remaining_data = "{:.1f}".format(remaining_data)
    if user_manager.get_user_language() == "en":
        subscription_type = subscription_data['type']
        type = {"free": "Free 🥉", "premium": "Premium 🥇"}
        if subscription_type == "free":
            days_left = "♾️"
        else:
            days_left = subscription_data['days_left']
        max_file_size = subscription_data['max_file_size']
        max_data_per_day = subscription_data['max_data_per_day']
        formatted_subscription_type = type[subscription_type]
        response = user_manager.return_response_based_on_language(english=english.subscription_details)
        response = response.format(formatted_subscription_type, days_left, max_file_size, max_data_per_day,
                                   formatted_used_data, formatted_remaining_data)

    elif user_manager.get_user_language() == "fa":
        subscription_type = subscription_data['type']
        type = {"free": "رایگان 🥉", "premium": "ویژه 🥇"}
        if subscription_type == "free":
            days_left = "♾️"
        else:
            days_left = subscription_data['days_left']
        formatted_subscription_type = type[subscription_type]
        max_file_size = subscription_data['max_file_size']
        max_data_per_day = subscription_data['max_data_per_day']
        response = user_manager.return_response_based_on_language(persian=persian.my_subscribtion_details)
        response = response.format(formatted_subscription_type, days_left, max_file_size, max_data_per_day,
                                   formatted_used_data, formatted_remaining_data)

        bot.send_message(msg.chat.id, response, parse_mode='markdown')
