from bot.user_management.utils.user_utils import UserManager
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


class KeyboardMarkupGenerator:
    def __init__(self, user_id):
        """
        initialize class with user_id
        :param user_id:
        The unique identifier of the user.
        """

        self.user_id = user_id
        self.user_language = UserManager(user_id).get_user_language()

    def _create_reply_keyboard(self, buttons):
        """
        Create ReplyKeyboardMarkup from list of buttons
        :param buttons:
        list of buttons (KeyboardButton)
        :return:
        ReplyKeyboardMarkup object
        """

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for row in buttons:
            markup.row(*row)
        return markup

    def _create_inline_keyboard(self, buttons):
        """
        Create InlineKeyboardMarkup from list of buttons
        :param buttons:
        list of buttons (InlineKeyboardButton)
        :return:
        InlineKeyboardMarkup object
        """

        markup = InlineKeyboardMarkup()
        for row in buttons:
            markup.row(row)
        return markup

    def homepage_buttons(self):
        """
        Create homepage buttons based on user language
        :return:
        list of buttons (KeyboardButton)
        """

        user_language = self.user_language
        if user_language == 'en':
            buttons = [[KeyboardButton("🛒 Buy Subscription")],
                       [KeyboardButton("📋 My Subscription"), KeyboardButton("👤 Account")],
                       [KeyboardButton("⚙️ Settings"), KeyboardButton("🎁 Gift Code")],
                       [KeyboardButton("📞 Support"), KeyboardButton("📖 Guide")]]
        else:
            buttons = [[KeyboardButton("🛒 خرید اشتراک")],
                       [KeyboardButton("📋 اشتراک من"), KeyboardButton("👤 حساب کاربری")],
                       [KeyboardButton("⚙️ تنظیمات"), KeyboardButton("🎁 کد هدیه")],
                       [KeyboardButton("📞 پشتیبانی"), KeyboardButton("📖 راهنما")]]
        return self._create_reply_keyboard(buttons)

    def return_buttons(self):
        """
        Create return button based on user language
        :return:
        list of buttons (KeyboardButton)
        """

        user_language = self.user_language
        if user_language == 'en':
            buttons = [[KeyboardButton(text="↩️ Return")]]
        else:
            buttons = [[KeyboardButton(text="↩️ بازگشت")]]
        return self._create_reply_keyboard(buttons)

    def settings_buttons(self):
        """
        Create settings buttons based on user language
        :return:
        list of buttons (KeyboardButton)
        """

        user_language = self.user_language
        if user_language == 'en':
            buttons = [[KeyboardButton("🌐 Change Language")], [KeyboardButton("↩️ Return")]]
        else:
            buttons = [[KeyboardButton("🌐 تغییر زبان")], [KeyboardButton("↩️ بازگشت")]]
        return self._create_reply_keyboard(buttons)

    def account_buttons(self):
        """
        Create account buttons based on user language
        :return:
        list of buttons (InlineButton)
        """

        user_language = self.user_language
        if user_language == 'en':
            buttons = [InlineKeyboardButton(text="💳 Charge Account", callback_data="charge_account"),
                       InlineKeyboardButton(text="📢 Invite Referrals", callback_data="invite_referrals")]
        else:
            buttons = [InlineKeyboardButton(text="💳 شارژ حساب", callback_data="charge_account"),
                       InlineKeyboardButton(text="📢 زیر مجموعه گیری", callback_data="invite_referrals")]
        return self._create_inline_keyboard(buttons)

    def my_subscription_buttons(self):
        """
        Create my subscription buttons based on user language
        :return:
        list of buttons (InlineButton)
        """

        user_language = self.user_language
        if user_language == 'en':
            buttons = [InlineKeyboardButton(text="❌ Auto Renew", callback_data="auto_renew")]
        else:
            buttons = [InlineKeyboardButton(text="❌ تمدید خودکار", callback_data="auto_renew")]
        return self._create_inline_keyboard(buttons)

    def subscribe_to_channel_buttons(self):
        """
        Create subscribe to channel buttons based on user language
        :return:
        list of buttons (InlineButton)
        """

        user_language = self.user_language
        channel_link = "https://t.me/DiarDev"
        if user_language == 'en':
            buttons = [InlineKeyboardButton("👉 Join Channel", url=channel_link),
                       InlineKeyboardButton("✅ I Joined", callback_data="check_joined")]
        else:
            buttons = [InlineKeyboardButton("👉 عضویت در کانال", url=channel_link),
                       InlineKeyboardButton("✅ عضو شدم", callback_data="check_joined")]
        return self._create_inline_keyboard(buttons)

    def subscriptions_list_buttons(self):
        """
        Create subscriptions list buttons based on user language
        :return:
        list of buttons (InlineButton)
        """
        user_language = self.user_language
        if user_language == 'en':
            buttons = [InlineKeyboardButton("🥇 Premium (30 Days)", callback_data="premium_30_in_list"),
                       InlineKeyboardButton("💎 Premium (60 Days)", callback_data="premium_60_in_list")]
        else:
            buttons = [InlineKeyboardButton("🥇 پرمیوم (30 روز)", callback_data="premium_30_in_list"),
                       InlineKeyboardButton("💎 پرمیوم (60 روز)", callback_data="premium_60_in_list")]
        return self._create_inline_keyboard(buttons)

    def subscription_details_buttons(self, subscription_info):
        """
        Create subscription details buttons based on user language
        :param subscription_info: pass in this format premium_30 or _60
        :return:
        list of buttons (InlineButton)
        """
        user_language = self.user_language
        if user_language == 'en':
            if subscription_info == "premium_30":
                buttons = [InlineKeyboardButton("💳 Direct Payment", callback_data="buy_premium_30_direct_payment"),
                           InlineKeyboardButton("🔋 From Account Charge", callback_data="buy_premium_30_account_charge")]
            elif subscription_info == "premium_60":
                buttons = [InlineKeyboardButton("💳 Buy Directly", callback_data="buy_premium_60_direct_payment"),
                           InlineKeyboardButton("🔋 From Account Charge", callback_data="buy_premium_60_account_charge")]
            buttons += [InlineKeyboardButton("↩️ Back", callback_data="back_to_subscriptions_list")]
        else:
            if subscription_info == "premium_30":
                buttons = [InlineKeyboardButton("💳 پرداخت مستقیم", callback_data="buy_premium_30_direct_payment"),
                           InlineKeyboardButton("🔋 پرداخت از شارژ حساب", callback_data="buy_premium_30_account_charge")]
            elif subscription_info == "premium_60":
                buttons = [InlineKeyboardButton("💳 پرداخت مستقیم", callback_data="buy_premium_60_direct_payment"),
                           InlineKeyboardButton("🔋 پرداخت از شارژ حساب", callback_data="buy_premium_60_account_charge")]
            buttons += [InlineKeyboardButton("↩️ بازگشت", callback_data="back_to_subscriptions_list")]

        return self._create_inline_keyboard(buttons)
