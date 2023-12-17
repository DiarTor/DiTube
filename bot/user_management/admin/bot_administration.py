import datetime

import jdatetime
import telebot
from config.database import users_collection, factors_collection
from languages import persian
from telebot.apihelper import ApiTelegramException


class BotAdministration:
    def __init__(self):
        self.admin = {1154909190}
        self.today = self._get_today_date()
        self.yesterday = self._get_yesterday_date()
        self.this_week = self._get_this_week_start_date()
        self.this_month = self._get_this_month_start_date()

    def _is_admin(self, user_id):
        return user_id in self.admin

    def _get_today_date(self):
        return jdatetime.date.today().strftime("%Y/%m/%d")

    def _get_yesterday_date(self):
        yesterday = jdatetime.date.today() - datetime.timedelta(days=1)
        return yesterday.strftime("%Y/%m/%d")

    def _get_this_week_start_date(self):
        today = jdatetime.date.today()
        this_week_start = today - datetime.timedelta(days=today.weekday())
        this_week_dates = [this_week_start + datetime.timedelta(days=i) for i in range(7)]
        return [date.strftime("%Y/%m/%d") for date in this_week_dates]

    def _get_this_month_start_date(self):
        return jdatetime.date.today().replace(day=1).strftime("%Y/%m/%d")

    def get_bot_stats(self, msg: telebot.types.Message, bot: telebot.TeleBot):
        if not self._is_admin(msg.from_user.id):
            return

        user_register_date_ranges = {"امروز": {"register_date": self.today}, "دیروز": {"register_date": self.yesterday},
                                     "این هفته": {"register_date": {"$in": self.this_week}},
                                     "این ماه": {"register_date": {"$gte": self.this_month}}, "کل": {}, }

        user_counts = {period: users_collection.count_documents(filter=date_filter) for period, date_filter in
                       user_register_date_ranges.items()}

        factors = {"امروز": {"check_date": self.today, "status": "confirmed"},
                   "دیروز": {"check_date": self.yesterday, "status": "confirmed"},
                   "این هفته": {"check_date": {"$in": self.this_week}, "status": "confirmed"},
                   "این ماه": {"check_date": {"$gte": self.this_month}, "status": "confirmed"},
                   "کل": {"status": "confirmed"}, }

        factors_sum = {}
        for period, factors_filter in factors.items():
            factors_cursor = factors_collection.find(factors_filter)
            total_price = sum(factor["price"] for factor in factors_cursor)
            formatted_total_price = f"{total_price:,}"
            factors_sum[period] = formatted_total_price

        payment_methods = {"درگاه مستقیم": {"payment_method": "payment_gateway", "status": "confirmed"},
                           "کارت به کارت": {"payment_method": "card_to_card", "status": "confirmed"},
                           "ارز دیجیتال": {"payment_method": "digital_currency", "status": "confirmed"}, }

        methods_income = {}
        for method, payment_methods_filter in payment_methods.items():
            payment_methods_cursor = factors_collection.find(payment_methods_filter)
            total_price = sum(factor["price"] for factor in payment_methods_cursor)
            formatted_total_price = f"{total_price:,}"
            methods_income[method] = formatted_total_price

        response = persian.stats.format(user_counts["امروز"], user_counts["دیروز"], user_counts["این هفته"],
                                        user_counts["این ماه"], user_counts["کل"], factors_sum["امروز"],
                                        factors_sum["دیروز"],
                                        factors_sum["این هفته"], factors_sum["این ماه"], factors_sum["کل"],
                                        methods_income['درگاه مستقیم'],
                                        methods_income['کارت به کارت'], methods_income['ارز دیجیتال'])

        bot.send_message(msg.chat.id, response, parse_mode="Markdown")

    def admin_commands_help(self, msg: telebot.types.Message, bot: telebot.TeleBot):
        if not self._is_admin(msg.from_user.id):
            return

        bot.send_message(msg.chat.id, persian.admin_commands_help)
