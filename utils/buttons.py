from telegram import KeyboardButton
from utils.check_user_settings import check_user_lang


def homepage_buttons(user_id):
    if check_user_lang(user_id) == "en":
        buttons = [[KeyboardButton("🛒 Buy Subscription")],
                   [KeyboardButton("📋 My Subscription"), KeyboardButton("👤 Account")],
                   [KeyboardButton("⚙️ Settings"), KeyboardButton("🎁 Gift Code")],
                   [KeyboardButton("🆘 Support"), KeyboardButton("📖 Guide")]]
    else:
        buttons = [[KeyboardButton("🛒 خرید اشتراک")], [KeyboardButton("📋 اشتراک من"), KeyboardButton("👤 حساب کاربری")],
                   [KeyboardButton("⚙️ تنظیمات"), KeyboardButton("🎁 کد هدیه")],
                   [KeyboardButton("🆘 پشتیبانی"), KeyboardButton("📖 راهنما")]]
    return buttons


def settings_buttons(user_id):
    if check_user_lang(user_id) == "en":
        buttons = [[KeyboardButton("Change Language")], [KeyboardButton("Return")]]
    else:
        buttons = [[KeyboardButton("تغییر زبان")], [KeyboardButton("بازگشت")]]
    return buttons
