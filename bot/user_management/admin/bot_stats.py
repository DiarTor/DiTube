import datetime

import telebot
from config.database import users_collection, factors_collection
from languages import persian
from persiantools.jdatetime import JalaliDate


class BotStats:
    def _get_today_date(self):
        return datetime.datetime.now().date().strftime("%Y-%m-%d")

    def _get_yesterday_date(self):
        yesterday = datetime.datetime.now().date() - datetime.timedelta(days=1)
        return yesterday.strftime("%Y-%m-%d")

    def _get_this_week_date(self):
        today = datetime.datetime.now().date()
        this_week_start = today - datetime.timedelta(days=today.weekday())
        this_week_dates = [this_week_start + datetime.timedelta(days=i) for i in range(7)]
        return [date.strftime("%Y-%m-%d") for date in this_week_dates]

    def _get_this_month_date(self):
        return datetime.date.today().replace(day=1).strftime("%Y-%m-%d")

    def _get_today_jdate(self):
        return JalaliDate.today().strftime("%Y-%m-%d")

    def _get_yesterday_jdate(self):
        yesterday = JalaliDate.today() - datetime.timedelta(days=1)
        return yesterday.strftime("%Y-%m-%d")

    def _get_this_week_jdate(self):
        today = JalaliDate.today()
        this_week_start = today - datetime.timedelta(days=today.weekday())
        this_week_dates = [this_week_start + datetime.timedelta(days=i) for i in range(7)]
        return [date.strftime("%Y-%m-%d") for date in this_week_dates]

    def _get_this_month_jdate(self):
        return JalaliDate.today().replace(day=1).strftime("%Y-%m-%d")

    def get_bot_stats(self):
        # users:
        today = self._get_today_date()
        yesterday = self._get_yesterday_date()
        this_week = self._get_this_week_date()
        this_month = self._get_this_month_date()

        user_register_date_ranges = {
            "امروز": {"register_date": today},
            "دیروز": {"register_date": yesterday},
            "این هفته": {"register_date": {"$in": this_week}},
            "این ماه": {"register_date": {"$gte": this_month}},
            "کل": {},
        }
        user_counts = {period: users_collection.count_documents(filter=date_filter) for period, date_filter in
                       user_register_date_ranges.items()}
        # factors:
        factors = {
            "امروز": {"check_date": self._get_today_jdate(), "status": "confirmed"},
            "دیروز": {"check_date": self._get_yesterday_jdate(), "status": "confirmed"},
            "این هفته": {"check_date": {"$in": self._get_this_week_jdate()}, "status": "confirmed"},
            "این ماه": {"check_date": {"$gte": self._get_this_month_jdate()}, "status": "confirmed"},
            "کل": {"status": "confirmed"},
        }
        factors_sum = {}
        for period, factors_filter in factors.items():
            factors_cursor = factors_collection.find(factors_filter)
            total_price = sum(factor["price"] for factor in factors_cursor)
            formatted_total_price = f"{total_price:,}"
            factors_sum[period] = formatted_total_price

        response = persian.stats.format(
            user_counts["امروز"], user_counts["دیروز"], user_counts["این هفته"],
            user_counts["این ماه"], user_counts["کل"], factors_sum["امروز"], factors_sum["دیروز"],
            factors_sum["این هفته"], factors_sum["این ماه"], factors_sum["کل"]
        )

        return response

    def process_command(self, msg: telebot.types.Message, bot: telebot.TeleBot):
        stats = self.get_bot_stats()
        bot.send_message(msg.chat.id, stats, parse_mode="Markdown")
        return
