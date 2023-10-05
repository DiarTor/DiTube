from bot.database import users_collection
from jdatetime import datetime as jdatetime
import datetime
def get_user_lang(user_id):
    return users_collection.find_one({"user_id": user_id})["settings"]["language"]


def get_user_subscription_data(user_id):
    return users_collection.find_one({"user_id": user_id})["subscription"]


def format_subscription_data(subscription_data, user_id):
    if get_user_lang(user_id=user_id) == "en":
        subscription_type = subscription_data['type']
        type = {
            "bronze": "Bronze 🥉",
            "silver": "Silver 🥈",
            "gold": "Gold 🥇",
            "diamond": "Diamond 💎",
        }
        subscription_status = subscription_data['status']
        status = {
            'active': "Active",
            'expired': "Expired",
        }
        formatted_data = f"📊 Subscription Details 📊\n\n"

        formatted_data += f"🔸 Type: {type[subscription_type]}\n"
        formatted_data += f"🟢 Status: {status[subscription_status]}\n"
        formatted_data += f"📅 Start Date: {subscription_data['start_date']}\n"

        if subscription_data['expire_date']:
            formatted_data += f"❌ Expire Date: {subscription_data['expire_date']}\n"
        else:
            formatted_data += f"❌ Expire Date: Never\n"

        formatted_data += f"🔄 Auto Renew: {'Yes' if subscription_data['auto_renew'] else 'No'}\n"
        formatted_data += f"📏 Max Size Per File: {subscription_data['max_size_per_file']} MB\n"
        formatted_data += f"📆 Max Size Per Month: {subscription_data['max_size_per_month']} MB\n"
        formatted_data += f"💾 Used Size: {subscription_data['used_size']} MB\n"
        formatted_data += f"💼 Remaining Size: {subscription_data['remaining_size']} MB\n"

        formatted_data += f"🌟 Features:\n"
        for feature in subscription_data['features']:
            formatted_data += f"  - {feature}\n"

        formatted_data += f"\n✨ To access more features, you can purchase a special subscription using the Buy Subscription button."
    else:
        subscription_type = subscription_data['type']
        type = {
            "bronze": "برونز 🥉",
            "silver": "نقره 🥈",
            "gold": "طلایی 🥇",
            "diamond": "الماس 💎",
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
        formatted_data += f"🔸 نوع : {type[subscription_type]}\n"
        formatted_data += f"🟢 وضعیت : {status[subscription_status]}\n"
        formatted_data += f"📅 تاریخ شروع : {formatted_jalali_start_date}\n"

        if subscription_data['expire_date']:
            formatted_data += f"❌ تاریخ انقضا : {formatted_jalali_expire_date}\n"
        else:
            formatted_data += f"❌ تاریخ انقضا : هیچوقت\n"

        formatted_data += f"🔄 تجدید خودکار : {'بله' if subscription_data['auto_renew'] else 'خیر'}\n"
        formatted_data += f"📏 حداکثر اندازه برای هر فایل : {subscription_data['max_size_per_file']} مگابایت\n"
        formatted_data += f"📆 حداکثر اندازه در ماه : {subscription_data['max_size_per_month']} مگابایت\n"
        formatted_data += f"💾 اندازه استفاده شده : {subscription_data['used_size']} مگابایت\n"
        formatted_data += f"💼 اندازه باقی‌مانده : {subscription_data['remaining_size']} مگابایت\n"

        formatted_data += f"\n✨ برای بهره برداری از امکانات بیشتر میتوانید با استفاده از دکمه خرید اشتراک, اشتراک ویژه تهیه کنید."
    return formatted_data
