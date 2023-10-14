import datetime

from bot.database import users_collection
from jdatetime import datetime as jdatetime


def get_user_lang(user_id):
    return users_collection.find_one({"user_id": user_id})["settings"]["language"]


def get_user_subscription_data(user_id):
    return users_collection.find_one({"user_id": user_id})["subscription"]


def format_subscription_data(subscription_data, user_id):
    used_data = subscription_data['used_data']
    remaining_data = subscription_data['remaining_data']
    formatted_used_data = "{:.2f}".format(used_data)
    formatted_remaining_data = "{:.2f}".format(remaining_data)
    if get_user_lang(user_id=user_id) == "en":
        subscription_type = subscription_data['type']
        type = {
            "bronze": "Bronze 🥉",
            "silver": "Silver 🥈",
            "gold": "Gold 🥇",
        }
        subscription_status = subscription_data['status']
        status = {
            'active': "Active",
            'expired': "Expired",
        }
        formatted_data = f"📊 Subscription Details 📊\n\n"
        formatted_data += "➖➖➖➖➖➖➖➖➖➖➖\n"
        formatted_data += f"🔸 Type: {type[subscription_type]}\n"
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

        formatted_data += f"🔄 Auto Renew: {'Yes' if subscription_data['auto_renew'] else 'No'}\n"
        formatted_data += f"📏 Max File Size: {subscription_data['max_file_size']} MB\n"
        formatted_data += f"📆 Max Data Per Month: {subscription_data['max_data_per_day']} MB\n"
        formatted_data += f"💾 Used Data: {formatted_used_data} MB\n"
        formatted_data += f"💼 Remaining Data: {formatted_remaining_data} MB\n"
        formatted_data += "➖➖➖➖➖➖➖➖➖➖➖\n"
        formatted_data += f"\n✨ To access more features, you can purchase a special subscription using the Buy Subscription button."
    else:
        subscription_type = subscription_data['type']
        type = {
            "bronze": "برونز 🥉",
            "silver": "نقره 🥈",
            "gold": "طلایی 🥇",
        }
        subscription_status = subscription_data['status']
        status = {
            'active': "فعال",
            'expired': "منقضی",
        }
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
        formatted_data = f"📊 جزئیات اشتراک 📊\n\n"
        formatted_data += "➖➖➖➖➖➖➖➖➖➖➖\n"
        formatted_data += f"🔸 نوع : {type[subscription_type]}\n"
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

        formatted_data += f"🔄 تجدید خودکار : {'بله' if subscription_data['auto_renew'] else 'خیر'}\n"
        formatted_data += f"📏 حداکثر حجم برای هر فایل : {subscription_data['max_file_size']} مگابایت\n"
        formatted_data += f"📆 حداکثر حجم در ماه : {subscription_data['max_data_per_day']} مگابایت\n"
        formatted_data += f"💾 حجم استفاده شده : {formatted_used_data} مگابایت\n"
        formatted_data += f"💼 حجم باقی‌مانده : {formatted_remaining_data} مگابایت\n"
        formatted_data += "➖➖➖➖➖➖➖➖➖➖➖\n"
        formatted_data += f"\n✨ برای بهره برداری از امکانات بیشتر میتوانید با استفاده از دکمه *خرید اشتراک* اشتراک ویژه تهیه کنید."
    return formatted_data
