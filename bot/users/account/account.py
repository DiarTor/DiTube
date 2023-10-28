import telebot.types
from bot.database import users_collection
from jdatetime import datetime as jdatetime
from utils.buttons import account_buttons
from utils.get_user_data import get_user_lang
import datetime

def show_account(msg: telebot.types.Message, bot: telebot.TeleBot):
    user = msg.from_user
    user_lang = get_user_lang(user_id=user.id)
    user_register_date = users_collection.find_one({"user_id": user.id})["registered_at"]
    user_total_downloads = len(users_collection.find_one({"user_id": user.id})["downloads"])
    user_total_downloads_size = sum(i.get("size", 0) for i in
                                    users_collection.find_one({"user_id": user.id}).get("downloads",
                                                                                        [])) if users_collection.find_one(
        {"user_id": user.id}) else 0
    formated_user_total_downloads_size = "{:.1f}".format(user_total_downloads_size)
    user_balance = users_collection.find_one({"user_id": user.id})["balance"]
    user_referrals = len(users_collection.find_one({"user_id": user.id})["referrals"])
    jalali_start_date = jdatetime.fromgregorian(
        datetime=datetime.datetime.strptime(user_register_date, "%Y-%m-%d %H:%M:%S"))
    user_jdate_register_date = jalali_start_date.strftime("%Y/%m/%d")
    buttons = account_buttons(user_id=user.id)
    response_english = ("👤 **Account Information**\n\n"
                        f"👥 User ID: `{user.id}`\n"
                        "🌍 Language: English 🇺🇸\n"
                        f"📅 Registered Since: {user_register_date}\n\n"
                        f"📥 Total Downloads: {user_total_downloads}\n"
                        f"💾 Total Downloads Size: {formated_user_total_downloads_size} MB\n\n"
                        f"💰 Balance: {user_balance} Toman\n"
                        f"🤝 Referrals: {user_referrals}\n\n"
                        f"🚀 To Charge Your Account, Use The '*'Charge Account'*' Button, And For Referral, Use The '*'Invite Users'*' Button!"
                        f"\n\n@MiTubeRobot")

    response_farsi = ("👤 **اطلاعات حساب**\n\n"
                      f"👥 شناسه کاربری: `{user.id}`\n"
                      "🌍 زبان: فارسی 🇮🇷\n"
                      f"📅 تاریخ عضویت: {user_jdate_register_date}\n\n"
                      f"📥 تعداد کل دانلودها: {user_total_downloads}\n"
                      f"💾 حجم کل دانلودها: {formated_user_total_downloads_size} مگابایت\n\n"
                      f"💰 موجودی: {user_balance} تومان\n"
                      f"🤝 تعداد زیر مجموعه ها: {user_referrals}\n\n"
                      "🚀 برای شارژ حساب کاربری خود از دکمه '*'شارژ حساب'*' استفاده کنید, و برای زیر مجموعه گیری از دکمه '*'زیر مجموعه گیری'*' اسفتاده کنید!"
                      f"\n\n@MiTubeRobot")

    if user_lang == "en":
        final_response = response_english
    else:
        final_response = response_farsi

    bot.send_message(chat_id=msg.chat.id, text=final_response, reply_markup=account_buttons(user.id),
                     parse_mode="markdown")
