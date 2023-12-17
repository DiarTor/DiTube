import telebot
from config.database import users_collection, factors_collection
from languages import persian
from telebot.apihelper import ApiTelegramException

class UserAdministration:
    def _is_admin(self, user_id):
        return user_id in {1154909190}

    def _get_user_by_id(self, user_id):
        return users_collection.find_one({"user_id": user_id})

    def _get_formatted_balance(self, user):
        return f"{user['balance']:,}"

    def _get_formatted_total_charges(self, total_money_charged):
        total_money_charged_to_toman = total_money_charged // 10
        return f"{total_money_charged_to_toman:,}"

    def include_user_balance(self, msg: telebot.types.Message, bot: telebot.TeleBot):
        if not self._is_admin(msg.from_user.id):
            return

        try:
            args = msg.text.split()[1:]
            user_id, credit, message = int(args[0]), int(args[1]), " ".join(args[2:])

            user = self._get_user_by_id(user_id)
            if user is None:
                bot.send_message(msg.chat.id, "❌ کاربری با این شماره کاربری وجود ندارد.")
                return

            user_old_balance = user["balance"]
            formatted_old_balance = self._get_formatted_balance(user)

            users_collection.update_one({"user_id": user_id}, {"$inc": {"balance": credit}})
            user_new_balance = user_old_balance + credit
            formatted_new_balance = f"{user_new_balance:,}"

            bot.send_message(msg.chat.id, f"✅ تغییر اعتبار با موفقیت انجام شد.\n"
                                          f"شماره کاربری: `{user_id}`\n"
                                          f"اعتبار قبلی: *{formatted_old_balance}* تومان\n"
                                          f"اعتبار جدید: *{formatted_new_balance}* تومان\n"
                                          f"پیام: *{message}*", parse_mode="Markdown")

            bot.send_message(user_id,
                             persian.your_balance_changed_by_admin.format(formatted_old_balance, formatted_new_balance,
                                                                          message), parse_mode="Markdown")
        except (IndexError, ValueError):
            bot.send_message(msg.chat.id,
                             "❌ لطفا دستور را به این صورت وارد کنید:\n /include_balance [User_id] [Credit] [Text]")

    def get_user_stat(self, msg: telebot.types.Message, bot: telebot.TeleBot):
        if not self._is_admin(msg.from_user.id):
            return

        try:
            args = msg.text.split()[1:]
            user_id = int(args[0])
            user = self._get_user_by_id(user_id)

            if user is None:
                bot.send_message(msg.chat.id, "❌ کاربری با این شماره کاربری وجود ندارد.")
                return

            user_factors = factors_collection.find({"user_id": user_id, "status": "confirmed"})

            user_total_downloads_size = sum(i.get("size", 0) for i in user.get("downloads", []))
            total_money_charged = sum(i.get("price", 0) for i in user_factors)

            formatted_balance = self._get_formatted_balance(user)
            formatted_total_charges = self._get_formatted_total_charges(total_money_charged)

            subscription_type = user['subscription']['type']
            subscription_days = user['subscription']['days'] if subscription_type != 'free' else None
            subscription_days_left = user['subscription']['days_left'] if subscription_type != 'free' else None

            user_stats = {"username": user["user_name"], "user_id": user["user_id"],
                          "register_date": user["register_date"], "downloads": len(user["downloads"]),
                          "downloads_size": user_total_downloads_size, "balance": formatted_balance,
                          "total_money_charged": formatted_total_charges, "referrals": user["referrals"],
                          "referral_total_profit": user["referral_total_profit"],
                          "subscription_type": subscription_type, "subscription_days": subscription_days,
                          "subscription_days_left": subscription_days_left, }

            response = persian.get_user_stat_message.format(user_stats["username"], user_stats["user_id"],
                                                            user_stats["register_date"], user_stats['downloads'],
                                                            user_stats["downloads_size"], user_stats["balance"],
                                                            user_stats["total_money_charged"], user_stats["referrals"],
                                                            user_stats["referral_total_profit"],
                                                            user_stats["subscription_type"],
                                                            user_stats["subscription_days"],
                                                            user_stats["subscription_days_left"])

            bot.send_message(msg.chat.id, response, parse_mode="Markdown")
        except (IndexError, ValueError):
            bot.send_message(msg.chat.id, "❌ لطفا دستور را به این صورت وارد کنید:\n/user_stat [User_id]")

    def send_message_to_user(self, msg: telebot.types.Message, bot: telebot.TeleBot):
        if not self._is_admin(msg.from_user.id):
            return

        try:
            args = msg.text.split()[1:]
            user_id, message = int(args[0]), " ".join(args[1:])
            message_template = persian.send_message_to_user_template
            bot.send_message(user_id, message_template.format(message), parse_mode="Markdown")
            bot.send_message(msg.chat.id, f"✅ پیام شما با موفقیت به کاربر `{user_id}` ارسال شد.", parse_mode="Markdown")
        except (IndexError, ValueError):
            bot.send_message(msg.chat.id,
                             "❌ لطفا دستور را به این صورت وارد کنید:\n/send_message_to_user [User_id] [Text]")

    def send_message_to_all_users(self, msg: telebot.types.Message, bot: telebot.TeleBot):
        if not self._is_admin(msg.from_user.id):
            return
        try:
            args = msg.text.split()
            msg.text = " ".join(args[1:])
            message = msg.text
            users = users_collection.find()
            for user in users:
                if user['user_id'] == 6967607104:
                    continue
                bot.send_message(user['user_id'], message, parse_mode="Markdown")
            bot.send_message(msg.chat.id, "✅ پیام شما به همه کاربران ارسال شد")
        except (IndexError, ValueError, ApiTelegramException) as e:
            bot.send_message(msg.chat.id, "❌ لطفا دستور را به این صورت وارد کنید:\n/send_message_to_all [Text]")

    def send_message_to_free_users(self, msg:telebot.types.Message, bot:telebot.TeleBot):
        if not self._is_admin(msg.from_user.id):
            return
        try:
            args = msg.text.split()
            msg.text = " ".join(args[1:])
            message = msg.text
            users = users_collection.find({"subscription.type": "free"})
            for user in users:
                if user['user_id'] == 6967607104:
                    continue
                bot.send_message(user['user_id'], message, parse_mode="Markdown")
            bot.send_message(msg.chat.id, "✅ پیام شما به همه کاربرانی که اشتراک *رایگان* دارند ارسال شد",parse_mode="Markdown")
        except (IndexError, ValueError, ApiTelegramException):
            bot.send_message(msg.chat.id, "❌ لطفا دستور را به این صورت وارد کنید:\n/send_message_to_free_users [Text]")
    def send_message_to_premium_users(self, msg:telebot.types.Message, bot:telebot.TeleBot):
        if not self._is_admin(msg.from_user.id):
            return
        try:
            args = msg.text.split()
            msg.text = " ".join(args[1:])
            message = msg.text
            users = users_collection.find({"subscription.type": "premium"})
            for user in users:
                if user['user_id'] == 6967607104:
                    continue
                bot.send_message(user['user_id'], message, parse_mode="Markdown")
            bot.send_message(msg.chat.id, "✅ پیام شما به همه کاربرانی که اشتراک *پرمیوم* دارند ارسال شد",parse_mode="Markdown")
        except (IndexError, ValueError, ApiTelegramException):
            bot.send_message(msg.chat.id, "❌ لطفا دستور را به این صورت وارد کنید:\n/send_message_to_premium_users [Text]")
