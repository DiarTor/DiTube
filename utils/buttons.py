from telegram import InlineKeyboardButton
from telegram import KeyboardButton
from utils.get_user_data import get_user_lang


def homepage_buttons(user_id):
    if get_user_lang(user_id) == "en":
        buttons = [[KeyboardButton("🛒 Buy Subscription")],
                   [KeyboardButton("📋 My Subscription"), KeyboardButton("👤 Account")],
                   [KeyboardButton("⚙️ Settings"), KeyboardButton("🎁 GiftCode")],
                   [KeyboardButton("📞 Support"), KeyboardButton("📖 Guide")]]
    else:
        buttons = [[KeyboardButton("🛒 خرید اشتراک")], [KeyboardButton("📋 اشتراک من"), KeyboardButton("👤 حساب کاربری")],
                   [KeyboardButton("⚙️ تنظیمات"), KeyboardButton("🎁 کد هدیه")],
                   [KeyboardButton("📞 پشتیبانی"), KeyboardButton("📖 راهنما")]]
    return buttons


def settings_buttons(user_id):
    if get_user_lang(user_id) == "en":
        buttons = [[KeyboardButton("🌐 Change Language")], [KeyboardButton("↩️ Return")]]
    else:
        buttons = [[KeyboardButton("🌐 تغییر زبان")], [KeyboardButton("↩️ بازگشت")]]

    return buttons


def account_buttons(user_id):
    if get_user_lang(user_id) == "en":
        buttons = [[InlineKeyboardButton(text="💳 Charge Account", callback_data="charge_account")],
                   [InlineKeyboardButton(text="📢 Invite Referrals", callback_data="invite_referrals")]]
    else:
        buttons = [[InlineKeyboardButton(text="💳 شارژ حساب", callback_data="charge_account")],
                   [InlineKeyboardButton(text="📢 زیر مجموعه گیری", callback_data="invite_referrals")]]
    return buttons


def my_subscription_buttons(user_id):
    if get_user_lang(user_id) == "en":
        buttons = [[InlineKeyboardButton(text="❌ Auto Renew", callback_data="auto_renew")]]
    else:
        buttons = [[InlineKeyboardButton(text="❌ تمدید خودکار", callback_data="auto_renew")]]
    return buttons


