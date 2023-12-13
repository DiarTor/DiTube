import datetime

import telebot
from config.database import users_collection

from languages import persian
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

    def get_bot_users(self):
        today = self._get_today_date()
        yesterday = self._get_yesterday_date()
        this_week = self._get_this_week_date()
        this_month = self._get_this_month_date()

        date_ranges = {
            "امروز": {"register_date": today},
            "دیروز": {"register_date": yesterday},
            "این هفته": {"register_date": {"$in": this_week}},
            "این ماه": {"register_date": {"$gte": this_month}},
            "کل": {},
        }
        user_counts = {period: users_collection.count_documents(filter=date_filter) for period, date_filter in
                       date_ranges.items()}

        response = persian.stats.format(user_counts["امروز"], user_counts["دیروز"], user_counts["این هفته"],
                                            user_counts["این ماه"], user_counts["کل"])

        return response

    def process_command(self, msg: telebot.types.Message, bot: telebot.TeleBot):
        users_sum = self.get_bot_users()
        bot.send_message(msg.chat.id, users_sum, parse_mode="Markdown")
        return
