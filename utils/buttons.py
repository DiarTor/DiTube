from telebot.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup
from utils.get_user_data import get_user_lang


def homepage_buttons(user_id):
    user_lang = get_user_lang(user_id)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if user_lang == "en":
        buttons = [[KeyboardButton("🛒 Buy Subscription")],
            [KeyboardButton("📋 My Subscription"), KeyboardButton("👤 Account")],
            [KeyboardButton("⚙️ Settings"), KeyboardButton("🎁 Gift Code")],
            [KeyboardButton("📞 Support"), KeyboardButton("📖 Guide")]]
    else:
        buttons = [[KeyboardButton("🛒 خرید اشتراک")], [KeyboardButton("📋 اشتراک من"), KeyboardButton("👤 حساب کاربری")],
            [KeyboardButton("⚙️ تنظیمات"), KeyboardButton("🎁 کد هدیه")],
            [KeyboardButton("📞 پشتیبانی"), KeyboardButton("📖 راهنما")]]
    for row in buttons:
        markup.row(*row)
    return markup


def settings_buttons(user_id):
    user_lang = get_user_lang(user_id)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if user_lang == "en":
        buttons = [[KeyboardButton("🌐 Change Language")], [KeyboardButton("↩️ Return")]]
    else:
        buttons = [[KeyboardButton("🌐 تغییر زبان")], [KeyboardButton("↩️ بازگشت")]]
    for row in buttons:
        markup.row(*row)
    return markup


def account_buttons(user_id):
    user_lang = get_user_lang(user_id)
    markup = InlineKeyboardMarkup()
    if get_user_lang(user_id) == "en":
        buttons = [
            InlineKeyboardButton(text="💳 Charge Account", callback_data="charge_account"),
            InlineKeyboardButton(text="📢 Invite Referrals", callback_data="invite_referrals")
        ]
    else:
        buttons = [
            InlineKeyboardButton(text="💳 شارژ حساب", callback_data="charge_account"),
            InlineKeyboardButton(text="📢 زیر مجموعه گیری", callback_data="invite_referrals")
        ]
    markup.row(*buttons)
    return markup


def my_subscription_buttons(user_id):
    user_lang = get_user_lang(user_id)
    markup = InlineKeyboardMarkup()
    if get_user_lang(user_id) == "en":
        buttons = [InlineKeyboardButton(text="❌ Auto Renew", callback_data="auto_renew")]
    else:
        buttons = [InlineKeyboardButton(text="❌ تمدید خودکار", callback_data="auto_renew")]
    markup.row(*buttons)
    return markup


def return_buttons(user_id):
    user_lang = get_user_lang(user_id)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if get_user_lang(user_id) == "en":
        buttons = [KeyboardButton(text="↩️ Return")]
    else:
        buttons = [KeyboardButton(text="↩️ بازگشت")]
    markup.row(*buttons)
    return markup