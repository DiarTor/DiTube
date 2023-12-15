from bot.user_management.account.charge_account_plans import AccountChargePlans
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


class KeyboardMarkupGenerator:
    def __init__(self, user_id):
        """
        initialize class with user_id
        :param user_id:
        The unique identifier of the user.
        """

        self.user_id = user_id

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
        Create homepage buttons
        :return:
        list of buttons (KeyboardButton)
        """

        buttons = [[KeyboardButton("🛒 خرید اشتراک")], [KeyboardButton("📋 اشتراک من")],
                   [KeyboardButton("🎁 کد هدیه"),KeyboardButton("👤 حساب کاربری"),],
                   [KeyboardButton("📞 پشتیبانی"), KeyboardButton("📖 راهنما")]]
        return self._create_reply_keyboard(buttons)

    def return_buttons(self):
        """
        Create return button
        :return:
        list of buttons (KeyboardButton)
        """

        buttons = [[KeyboardButton(text="↩️ بازگشت")]]
        return self._create_reply_keyboard(buttons)

    def settings_buttons(self):
        """
        Create settings buttons
        :return:
        list of buttons (KeyboardButton)
        """

        buttons = [[KeyboardButton("🌐 تغییر زبان")], [KeyboardButton("↩️ بازگشت")]]
        return self._create_reply_keyboard(buttons)

    def account_buttons(self):
        """
        Create account buttons
        :return:
        list of buttons (InlineButton)
        """

        buttons = [InlineKeyboardButton(text="💳 شارژ حساب", callback_data="charge_account"),
                   InlineKeyboardButton(text="📢 زیر مجموعه گیری", callback_data="invite_referrals")]
        return self._create_inline_keyboard(buttons)

    def my_subscription_buttons(self):
        """
        Create my subscription buttons
        :return:
        list of buttons (InlineButton)
        """

        buttons = [InlineKeyboardButton(text="❌ تمدید خودکار", callback_data="auto_renew")]
        return self._create_inline_keyboard(buttons)

    def subscribe_to_channel_buttons(self):
        """
        Create subscribe to channel buttons
        :return:
        list of buttons (InlineButton)
        """

        channel_link = "https://t.me/DiTube"
        buttons = [InlineKeyboardButton("👉 عضویت در کانال", url=channel_link),
                   InlineKeyboardButton("✅ عضو شدم", callback_data="check_joined")]
        return self._create_inline_keyboard(buttons)

    def subscriptions_list_buttons(self):
        """
        Create subscriptions list buttons
        :return:
        list of buttons (InlineButton)
        """
        buttons = [InlineKeyboardButton("🥇 پرمیوم (30 روز)", callback_data="id_1_in_list"),
                   InlineKeyboardButton("💎 پرمیوم (90 روز)", callback_data="id_2_in_list")]
        return self._create_inline_keyboard(buttons)

    def subscription_details_buttons(self, subscription_info):
        """
        Create subscription details buttons
        :param subscription_info: pass in this format premium_30 or _60
        :return:
        list of buttons (InlineButton)
        """
        if subscription_info == "id_1":
            buttons = [InlineKeyboardButton("💳 پرداخت مستقیم", callback_data="buy_id_1_direct_payment"),
                       InlineKeyboardButton("🔋 پرداخت از شارژ حساب", callback_data="buy_id_1_account_charge")]
        elif subscription_info == "id_2":
            buttons = [InlineKeyboardButton("💳 پرداخت مستقیم", callback_data="buy_id_2_direct_payment"),
                       InlineKeyboardButton("🔋 پرداخت از شارژ حساب", callback_data="buy_id_2_account_charge")]
        buttons += [InlineKeyboardButton("↩️ بازگشت", callback_data="back_to_subscriptions_list")]

        return self._create_inline_keyboard(buttons)

    def charge_account_buttons(self):
        """
        Create charge account buttons
        :return:
        list of buttons (InlineButton)
        """
        buttons = [InlineKeyboardButton("💳 شارژ حساب", callback_data="charge_account")]
        return self._create_inline_keyboard(buttons)

    def post_caption_buttons(self, channel_url, post_url):
        """
        Create post caption buttons
        :return:
        list of buttons (InlineButton)
        """
        buttons = [InlineKeyboardButton("🆑 | کانال یوتیوب سازنده", url=channel_url),
                   InlineKeyboardButton("🎥 | تماشا در یوتیوب", url=post_url)]
        return self._create_inline_keyboard(buttons)

    def charge_account_methods_buttons(self):
        """
        Create charge account methods buttons
        :return:
        list of buttons (InlineButton)
        """
        buttons = [InlineKeyboardButton("📲 درگاه پرداخت", callback_data="payment_gateway"),
                   InlineKeyboardButton("💳 کارت به کارت", callback_data="card_to_card"),
                   InlineKeyboardButton("💲 ارز دیجیتال", callback_data="digital_currency")]
        buttons += [InlineKeyboardButton("↩️ بازگشت", callback_data="return_to_my_account")]

        return self._create_inline_keyboard(buttons)

    def charge_account_plans_buttons(self, method):
        """
        Create charge account plans buttons
        m is method
        p is price
        :return:
        list of buttons (InlineButton)
        """
        buttons = []
        for i in AccountChargePlans.plans:
            format_number_with_commas = lambda number: f"{number:,}"
            formatted_price = format_number_with_commas(i)
            button = InlineKeyboardButton(text=f"💵 {str(formatted_price)} تومان",
                                          callback_data=f"m:{method} p:{str(i)}")
            buttons.append(button)
        buttons += [InlineKeyboardButton(text="↩️ بازگشت", callback_data="return_to_charge_methods")]
        return self._create_inline_keyboard(buttons)

    def send_factor_to_admins_buttons(self, factor_id):
        """
        Create send factor to admins buttons
        :return:
        list of buttons (InlineButton)
        """
        buttons = [InlineKeyboardButton(text="✅ تایید", callback_data=f"confirm_factor {factor_id}"),
                   InlineKeyboardButton(text="❌ رد", callback_data=f"deny_factor {factor_id}")]

        return self._create_inline_keyboard(buttons)
