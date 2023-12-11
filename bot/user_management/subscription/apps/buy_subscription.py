import re

import telebot
from bot.user_management.subscription.plans import Plans
from bot.common.button_utils import KeyboardMarkupGenerator
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
        if subscription == 'id_1':
            sub = self.plans[1]
        elif subscription == 'id_2':
            sub = self.plans[2]
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
        response = response.format(sub['days'], formatted_max_data_per_day, formatted_max_file_size, formatted_price,
                                   discount_precent,
                                   formatted_discount_price, formatted_user_balance, formatted_final_price)
        bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=response, reply_markup=keyboard,
                              parse_mode='Markdown')

    def subscriptions_list(self, msg: telebot.types.Message, bot: telebot.TeleBot, user_id):
        keyboard = KeyboardMarkupGenerator(user_id)
        user_manager = UserManager(user_id)
        response = user_manager.return_response_based_on_language(english=english.subscriptions_list,
                                                                  persian=persian.subscriptions_list)
        bot.send_message(msg.chat.id, response, reply_markup=keyboard.subscriptions_list_buttons())

    def buy_via_account_charge(self, msg: telebot.types.Message, bot: telebot.TeleBot, subscription, user_id, msg_id):
        if re.search("id_1", subscription):
            the_user = users_collection.find_one({"user_id": user_id})
            sub = self.plans[1]
            sub_price = self.id_1_final_price
            user_balance = users_collection.find_one({"user_id": user_id})['balance']
            if user_balance < sub_price:
                keyboard = KeyboardMarkupGenerator(user_id).charge_account_buttons()
                response = UserManager(user_id).return_response_based_on_language(
                    persian=persian.insufficient_balance, english=english.insufficient_balance)
                bot.send_message(msg.chat.id, response, reply_markup=keyboard, parse_mode='Markdown')
                return
            elif user_balance >= sub_price:
                if users_collection.find_one({"user_id": user_id})['subscription']['type'] == "free":
                    users_collection.update_one({"user_id": user_id}, {"$inc": {"balance": -sub_price}})
                    users_collection.update_one({"user_id": user_id}, {"$set": {"subscription": sub}})
                    response = UserManager(user_id).return_response_based_on_language(
                        persian=persian.subscription_bought, english=english.subscription_bought)
                    if UserManager(user_id).get_user_language() == 'en':
                        formatted_price = "{:,}".format(sub_price)
                        response = response.format("30-day premium", formatted_price)
                    elif UserManager(user_id).get_user_language() == 'fa':
                        formatted_price = "{:,}".format(sub_price)
                        response = response.format("پرمیوم 30 روزه", formatted_price)
                    bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=response, parse_mode='Markdown')
                else:
                    response = UserManager(user_id).return_response_based_on_language(
                        persian=persian.subscription_already_bought.format("پرمیوم"), english=english.subscription_already_bought.format("Premium"))
                    bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=response, parse_mode='Markdown')
        elif re.search("id_2", subscription):
            sub = self.plans[2]
            sub_price = self.id_2_final_price
            user_balance = users_collection.find_one({"user_id": user_id})['balance']
            if user_balance < sub_price:
                keyboard = KeyboardMarkupGenerator(user_id).charge_account_buttons()
                response = UserManager(user_id).return_response_based_on_language(
                    persian=persian.insufficient_balance, english=english.insufficient_balance)
                bot.send_message(msg.chat.id, response, reply_markup=keyboard, parse_mode='Markdown')
                return
            elif user_balance >= sub_price:
                if users_collection.find_one({"user_id": user_id})['subscription']['type'] == "free":
                    users_collection.update_one({"user_id": user_id}, {"$inc": {"balance": -sub_price}})
                    users_collection.update_one({"user_id": user_id}, {"$set": {"subscription": sub}})
                    response = UserManager(user_id).return_response_based_on_language(
                        persian=persian.subscription_bought, english=english.subscription_bought)
                    if UserManager(user_id).get_user_language() == 'en':
                        formatted_price = "{:,}".format(sub_price)
                        response = response.format("90-day premium", formatted_price)
                    elif UserManager(user_id).get_user_language() == 'fa':
                        formatted_price = "{:,}".format(sub_price)
                        response = response.format("پرمیوم 90 روزه", formatted_price)
                    bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=response, parse_mode='Markdown')
                else:
                    response = UserManager(user_id).return_response_based_on_language(
                        persian=persian.subscription_already_bought.format("پرمیوم"), english=english.subscription_already_bought.format("Premium"))
                    bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=response, parse_mode='Markdown')
