import datetime

import telebot.types
from jdatetime import datetime as jdatetime
from utils.button_utils import KeyboardMarkupGenerator
from utils.user_utils import UserManager
from langs import persian


def show_user_subscription_details(msg: telebot.types.Message, bot: telebot.TeleBot):
    user_manager = UserManager(msg.from_user.id)
    subscription_data = user_manager.get_user_subscription_details()
    used_data = subscription_data['used_data']
    remaining_data = subscription_data['remaining_data']
    formatted_used_data = "{:.1f}".format(used_data)
    formatted_remaining_data = "{:.1f}".format(remaining_data)
    if user_manager.get_user_language() == "en":
        subscription_type = subscription_data['type']
        type = {"bronze": "Bronze 🥉", "silver": "Silver 🥈", "gold": "Gold 🥇", }
        subscription_status = subscription_data['status']
        status = {'active': "Active", 'expired': "Expired", }
        formatted_data = f"🔸 Type: {type[subscription_type]}\n"
        formatted_data += f"🟢 Status: {status[subscription_status]}\n"
        if subscription_data['price'] == 0:
            formatted_data += f"💲 Price: Free \n"
        else:
            formatted_data += f"💲 Price: {subscription_data['price']} IRR\n"
        formatted_data += f"📅 Start Date: {subscription_data['start_date']}\n"

        if subscription_data['expire_date']:
            formatted_data += f"❌ Expire Date: {subscription_data['expire_date']}\n"
        else:
            formatted_data += f"❌ Expire Date: Never\n"

        formatted_data += f"📏 Max File Size: {subscription_data['max_file_size']} MB\n"
        formatted_data += f"📆 Max Data Per Day: {subscription_data['max_data_per_day']} MB\n"
        formatted_data += f"💾 Used Data: {formatted_used_data} MB\n"
        formatted_data += f"💼 Remaining Data: {formatted_remaining_data} MB\n"
        formatted_data += "➖➖➖➖➖➖➖➖➖➖\n"
        formatted_data += f"\n✨If you want your subscription to be automatically renewed at a 10% discount after it expires, activate the 'Auto Renew' option."
        formatted_data += f"\n\n@MiTubeRobot"
    else:
        subscription_type = subscription_data['type']
        type = {"bronze": "برونز 🥉", "silver": "نقره 🥈", "gold": "طلایی 🥇", }
        subscription_status = subscription_data['status']
        status = {'active': "فعال", 'expired': "منقضی", }
        subscription_start_date = subscription_data['start_date']
        subscription_expire_date = subscription_data['expire_date']
        jalali_start_date = jdatetime.fromgregorian(
            datetime=datetime.datetime.strptime(subscription_start_date, "%Y-%m-%d %H:%M:%S"))
        formatted_jalali_start_date = jalali_start_date.strftime("%Y/%m/%d")
        if subscription_data['expire_date']:
            subscription_expire_date = subscription_data['expire_date']
            jalali_expire_date = jdatetime.fromgregorian(
                datetime=datetime.datetime.strptime(subscription_expire_date, "%Y-%m-%d %H:%M:%S"))
            formatted_jalali_expire_date = jalali_expire_date.strftime("%Y/%m/%d")
        else:
            formatted_jalali_expire_date = "هیچوقت"
        formatted_subscription_type = type[subscription_type]
        formatted_subscription_status = status[subscription_status]
        if subscription_data['price'] == 0:
            formatted_price = "رایگان"
        else:
            formatted_price = subscription_data['price']

        max_file_size = subscription_data['max_file_size']
        max_data_per_day = subscription_data['max_data_per_day']
        response = user_manager.return_response_based_on_language(persian=persian.subscription_details)
        response = response.format(
            formatted_subscription_type,
            formatted_subscription_status,
            formatted_price,
            formatted_jalali_start_date,
            formatted_jalali_expire_date,
            max_file_size,
            max_data_per_day,
            formatted_used_data,
            formatted_remaining_data,

        )
    bot.send_message(msg.chat.id, response,
                     reply_markup=KeyboardMarkupGenerator(msg.from_user.id).my_subscription_buttons(),
                     parse_mode='markdown')
