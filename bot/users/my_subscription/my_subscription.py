import datetime

import telebot.types
from jdatetime import datetime as jdatetime
from utils.buttons import my_subscription_buttons
from utils.get_user_data import get_user_subscription_data, get_user_lang


def show_user_subscription_details(msg: telebot.types.Message, bot: telebot.TeleBot):
    subscription_data = get_user_subscription_data(user_id=msg.from_user.id)
    used_data = subscription_data['used_data']
    remaining_data = subscription_data['remaining_data']
    formatted_used_data = "{:.1f}".format(used_data)
    formatted_remaining_data = "{:.1f}".format(remaining_data)
    if get_user_lang(user_id=msg.from_user.id) == "en":
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
        formatted_data = f"🔸 نوع : {type[subscription_type]}\n"
        formatted_data += f"🟢 وضعیت : {status[subscription_status]}\n"
        if subscription_data['price'] == 0:
            formatted_data += f"💲 قیمت : رایگان\n"
        else:
            formatted_data += f"💲 قیمت : {subscription_data['price']} ریال\n"
        formatted_data += f"📅 تاریخ شروع : {formatted_jalali_start_date}\n"

        if subscription_data['expire_date']:
            formatted_data += f"❌ تاریخ انقضا : {formatted_jalali_expire_date}\n"
        else:
            formatted_data += f"❌ تاریخ انقضا : هیچوقت\n"

        formatted_data += f"📏 حداکثر حجم برای هر فایل : {subscription_data['max_file_size']} مگابایت\n"
        formatted_data += f"📆 حداکثر حجم در روز : {subscription_data['max_data_per_day']} مگابایت\n"
        formatted_data += f"💾 حجم استفاده شده : {formatted_used_data} مگابایت\n"
        formatted_data += f"💼 حجم باقی‌مانده : {formatted_remaining_data} مگابایت\n"
        formatted_data += "➖➖➖➖➖➖➖➖➖➖➖\n"
        formatted_data += f"\n✨در صورتی که تمایل دارید پس از تمام شدن زمان اشتراک، اشتراک شما با 10 درصد تخفیف بصورت خودکار تمدید شود، گزینه تمدید خودکار را فعال کنید."
        formatted_data += f"\n\n@MiTubeRobot"
    bot.send_message(msg.chat.id, formatted_data, reply_markup=my_subscription_buttons(msg.from_user.id), parse_mode='markdown')
