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

    def _get_this_week_start_date(self):
        today = datetime.datetime.now().date()
        this_week_start = today - datetime.timedelta(days=today.weekday())
        this_week_dates = [this_week_start + datetime.timedelta(days=i) for i in range(7)]
        return [date.strftime("%Y-%m-%d") for date in this_week_dates]

    def _get_this_month_start_date(self):
        return datetime.date.today().replace(day=1).strftime("%Y-%m-%d")

    def _get_today_jdate(self):
        return JalaliDate.today().strftime("%Y-%m-%d")

    def _get_yesterday_jdate(self):
        yesterday = JalaliDate.today() - datetime.timedelta(days=1)
        return yesterday.strftime("%Y-%m-%d")

    def _get_this_week_start_jdate(self):
        today = JalaliDate.today()
        this_week_start = today - datetime.timedelta(days=today.weekday())
        this_week_dates = [this_week_start + datetime.timedelta(days=i) for i in range(7)]
        return [date.strftime("%Y-%m-%d") for date in this_week_dates]

    def _get_this_month_start_jdate(self):
        return JalaliDate.today().replace(day=1).strftime("%Y-%m-%d")

    def get_bot_stats(self, msg: telebot.types.Message, bot: telebot.TeleBot):
        # users:
        today = self._get_today_date()
        yesterday = self._get_yesterday_date()
        this_week = self._get_this_week_start_date()
        this_month = self._get_this_month_start_date()

        user_register_date_ranges = {
            "امروز": {"register_date": today},
            "دیروز": {"register_date": yesterday},
            "این هفته": {"register_date": {"$in": this_week}},
            "این ماه": {"register_date": {"$gte": this_month}},
            "کل": {},
        }
        user_counts = {period: users_collection.count_documents(filter=date_filter) for period, date_filter in
                       user_register_date_ranges.items()}
        # income:
        factors = {
            "امروز": {"check_date": self._get_today_jdate(), "status": "confirmed"},
            "دیروز": {"check_date": self._get_yesterday_jdate(), "status": "confirmed"},
            "این هفته": {"check_date": {"$in": self._get_this_week_start_jdate()}, "status": "confirmed"},
            "این ماه": {"check_date": {"$gte": self._get_this_month_start_jdate()}, "status": "confirmed"},
            "کل": {"status": "confirmed"},
        }
        factors_sum = {}
        for period, factors_filter in factors.items():
            factors_cursor = factors_collection.find(factors_filter)
            total_price = sum(factor["price"] for factor in factors_cursor)
            formatted_total_price = f"{total_price:,}"
            factors_sum[period] = formatted_total_price

        # total income from all payment methods
        payment_methods = {
            "درگاه مستقیم": {"payment_method": "payment_gateway", "status": "confirmed"},
            "کارت به کارت": {"payment_method": "card_to_card", "status": "confirmed"},
            "ارز دیجیتال": {"payment_method": "digital_currency", "status": "confirmed"},
        }
        methods_income = {}
        for method, payment_methods in payment_methods.items():
            payment_methods_cursor = factors_collection.find(payment_methods)
            total_price = sum(factor["price"] for factor in payment_methods_cursor)
            formatted_total_price = f"{total_price:,}"
            methods_income[method] = formatted_total_price

        # final response
        response = persian.stats.format(
            user_counts["امروز"], user_counts["دیروز"], user_counts["این هفته"],
            user_counts["این ماه"], user_counts["کل"], factors_sum["امروز"], factors_sum["دیروز"],
            factors_sum["این هفته"], factors_sum["این ماه"], factors_sum["کل"], methods_income['درگاه مستقیم'],
            methods_income['کارت به کارت'], methods_income['ارز دیجیتال']
        )

        bot.send_message(msg.chat.id, response, parse_mode="Markdown")

    def include_user_balance(self, msg: telebot.types.Message, bot: telebot.TeleBot):
        try:
            args = msg.text.split()[1:]
            user_id = int(args[0])
            credit = int(args[1])
            message = str(args[2])
            user_old_balance = users_collection.find_one({"user_id": user_id})["balance"]
            formatted_old_balance = f"{user_old_balance:,}"
            users_collection.update_one({"user_id": user_id}, {"$inc": {"balance": credit}})
            user_new_balance = users_collection.find_one({"user_id": user_id})["balance"]
            formatted_new_balance = f"{user_new_balance:,}"
            bot.send_message(msg.chat.id,
                             "✅ تغییر اعتبار با موفقیت انجام شد.\n شماره کاربری: `{}`\nاعتبار قبلی: *{}* تومان\nاعتبار جدید: *{}* تومان\n پیام: *{}*".format(
                                 user_id, formatted_old_balance, formatted_new_balance, message), parse_mode="Markdown")
            bot.send_message(user_id,
                             persian.your_balance_changed_by_admin.format(formatted_old_balance, formatted_new_balance,
                                                                          message), parse_mode="Markdown")
        except IndexError:
            bot.send_message(msg.chat.id,
                             "❌ لطفا دستور را به این صورت وارد کنید:\n /inc_balance [ایدی عددی کاربر] [اعتبار] [پیام]")

    def get_user_stat(self, msg: telebot.types.Message, bot: telebot.TeleBot):
        try:
            args = msg.text.split()[1:]
            user_id = int(args[0])
            user = users_collection.find_one({"user_id": user_id})
            user_factors = factors_collection.find({"user_id": user_id, "status": "confirmed"})
            if user is None:
                bot.send_message(msg.chat.id, "❌ کاربری با این شماره کاربری وجود ندارد.")
                return
            user_total_downloads_size = sum(i.get("size", 0) for i in
                                            user.get("downloads", []))
            total_money_charged = sum(i.get("price", 0) for i in user_factors)
            formatted_balance = f"{user['balance']:,}"
            total_money_charged_to_toman = total_money_charged // 10
            formatted_total_charges = f"{total_money_charged_to_toman:,}"
            if user['subscription']['type'] != 'free':
                subscription_days = user['subscription']['days']
                subscription_days_left = user['subscription']['days_left']
            else:
                subscription_days = None
                subscription_days_left = None
            user_stats = {
                "username": user["user_name"],
                "user_id": user["user_id"],
                "register_date": user["register_date"],
                "downloads": len(user["downloads"]),
                "downloads_size": user_total_downloads_size,
                "balance": formatted_balance,
                "total_money_charged": formatted_total_charges,
                "referrals": user["referrals"],
                "referral_total_profit": user["referral_total_profit"],
                "subscription_type": user["subscription"]["type"],
                "subscription_days": subscription_days,
                "subscription_days_left": subscription_days_left,
            }
            response = persian.get_user_stat_message.format(user_stats["username"], user_stats["user_id"],
                                                            user_stats["register_date"], user_stats['downloads'],
                                                            user_stats["downloads_size"], user_stats["balance"],
                                                            user_stats["total_money_charged"],
                                                            user_stats["referrals"],
                                                            user_stats["referral_total_profit"],
                                                            user_stats["subscription_type"],
                                                            user_stats["subscription_days"],
                                                            user_stats["subscription_days_left"])
            bot.send_message(msg.chat.id, response, parse_mode="Markdown")
        except IndexError as e:
            print(e)
            bot.send_message(msg.chat.id, "❌ لطفا دستور را به این صورت وارد کنید:\n /user_stat [ایدی عددی کاربر]")
# todo : seperate inc_balance, get_user_stat from this class