import re

import telebot
from bot.user_management.subscription.plans import Plans
from bot.user_management.utils.button_utils import KeyboardMarkupGenerator
from bot.user_management.utils.user_utils import UserManager
from config.database import users_collection
from languages import persian, english


class BuySubscription(Plans):
    def return_to_subscriptions_list(self, msg: telebot.types.Message, bot: telebot.TeleBot, user_id):
        keyboard = KeyboardMarkupGenerator(user_id)
        user_manager = UserManager(user_id)
        response = user_manager.return_response_based_on_language(english=english.subscriptions_list,
                                                                  persian=persian.subscriptions_list)
        bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=response,
                              reply_markup=keyboard.subscriptions_list_buttons())

    def show_subscription_details(self, msg: telebot.types.Message, bot: telebot.TeleBot, subscription, user_id):
        keyboard = KeyboardMarkupGenerator(user_id).subscription_details_buttons(subscription)
        response = UserManager(user_id).return_response_based_on_language(persian=persian.subscription_details,
                                                                                   english=english.subscriptions_details)
        format_number_with_commas = lambda number: f"{number:,}"
        if subscription == 'premium_30':
            sub = self.premium_30
        elif subscription == 'premium_60':
            sub = self.premium_60
        formatted_max_data_per_day = sub['max_data_per_day'] // 1000
        formatted_max_file_size = sub['max_file_size'] // 1000
        user_balance = users_collection.find_one({"user_id": user_id})['balance']
        formatted_user_balance = format_number_with_commas(user_balance)
        formatted_price = format_number_with_commas(sub['price'])
        discount_precent = sub['discount_percent']
        discount_price = sub['price'] * discount_precent // 100
        formatted_discount_price = format_number_with_commas(discount_price)
        final_price = sub['price'] - discount_price
        formatted_final_price = format_number_with_commas(final_price)
        response = response.format(sub['days'], formatted_max_data_per_day, formatted_max_file_size, formatted_price, discount_precent,
                                   formatted_discount_price, formatted_user_balance, formatted_final_price)
        bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=response, reply_markup=keyboard,
                              parse_mode='Markdown')

    def list_subscriptions(self, msg: telebot.types.Message, bot: telebot.TeleBot, user_id):
        keyboard = KeyboardMarkupGenerator(user_id)
        user_manager = UserManager(user_id)
        response = user_manager.return_response_based_on_language(english=english.subscriptions_list,
                                                                  persian=persian.subscriptions_list)
        bot.send_message(msg.chat.id, response, reply_markup=keyboard.subscriptions_list_buttons())

    def buy_via_account_charge(self, msg: telebot.types.Message, bot: telebot.TeleBot, subscription, user_id):
        if re.search("premium_30", subscription):
            sub = self.premium_30
            sub_price = self.premiun_30_final_price
            user_balance = users_collection.find_one({"user_id": user_id})['balance']
            if user_balance < sub_price:
                response = UserManager(user_id).return_response_based_on_language(
                    persian=persian.insufficient_balance, english=english.insufficient_balance)
                bot.send_message(msg.chat.id, response, parse_mode='Markdown')
                return
            elif user_balance >= sub_price:
                if users_collection.find_one({"user_id": user_id})['subscription']['type'] == "free":
                    users_collection.update_one({"user_id": user_id}, {"$inc": {"balance": -sub_price}})
                    users_collection.update_one({"user_id": user_id}, {"$set": {"subscription": sub}})
                    response = UserManager(user_id).return_response_based_on_language(
                        persian=persian.subscription_bought, english=english.subscription_bought)
                    bot.send_message(msg.chat.id, response, parse_mode='Markdown')
                else:
                    response = UserManager(user_id).return_response_based_on_language(
                        persian=persian.subscription_already_bought, english=english.subscription_already_bought)
                    bot.send_message(msg.chat.id, response, parse_mode='Markdown')
        elif re.search("premium_60", subscription):
            sub = self.premium_60
            sub_price = self.premiun_60_final_price
            user_balance = users_collection.find_one({"user_id": user_id})['balance']
            if user_balance < sub_price:
                response = UserManager(user_id).return_response_based_on_language(
                    persian=persian.insufficient_balance, english=english.insufficient_balance)
                bot.send_message(msg.chat.id, response, parse_mode='Markdown')
                return
            elif user_balance >= sub_price:
                if users_collection.find_one({"user_id": user_id})['subscription']['type'] == "free":
                    users_collection.update_one({"user_id": user_id}, {"$inc": {"balance": -sub_price}})
                    users_collection.update_one({"user_id": user_id}, {"$set": {"subscription": sub}})
                    response = UserManager(user_id).return_response_based_on_language(
                        persian=persian.subscription_bought, english=english.subscription_bought)
                    bot.send_message(msg.chat.id, response, parse_mode='Markdown')
                else:
                    response = UserManager(user_id).return_response_based_on_language(
                        persian=persian.subscription_already_bought, english=english.subscription_already_bought)
                    bot.send_message(msg.chat.id, response, parse_mode='Markdown')
