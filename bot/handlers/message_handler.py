import re

import telebot.types
from bot.database import users_collection
from bot.handlers.yt_link_handler import youtube_video_handler
from bot.users.account.account import show_account
from bot.users.giftcode.giftcode import redeem_giftcode
from bot.users.my_subscription.my_subscription import show_user_subscription_details
from bot.users.settings.language import join_in_selecting_lang
from bot.users.settings.language import selected_lang_is_en, selected_lang_is_fa
from bot.users.settings.settings import join_in_settings
from bot.users.support.support import join_in_support, send_user_msg_to_support, send_user_photo_to_support, \
    reply_to_user_support_msg
from langs import persian, english
from utils.button_utils import KeyboardMarkupGenerator
from utils.user_utils import UserManager


def handle_user_message(msg: telebot.types.Message, bot: telebot.TeleBot):
    user = msg.from_user
    the_user = users_collection.find_one({"user_id": user.id})
    chat_id = msg.chat.id
    user_message = msg
    user_message_text = msg.text
    user_photo = msg.photo
    user_reply = msg.reply_to_message
    support_group_id = -4043182903
    keyboardgenerator = KeyboardMarkupGenerator(user.id)
    usermanager = UserManager(user.id)
    if not usermanager.is_subscribed_to_channel(msg, bot):
        response = usermanager.return_response_based_on_language(persian=persian.subscribe_to_channel)
        bot.send_message(chat_id, response, reply_markup=keyboardgenerator.subscribe_to_channel_buttons())
        return
    if not users_collection.find_one({"user_id": user.id}):
        bot.reply_to(msg, f"{persian.restart_required}\n\n{english.restart}")
    if chat_id == support_group_id and msg.reply_to_message:
        reply_to_user_support_msg(msg, bot)
    elif any(re.search(pattern, user_message_text) for pattern in [
        r'https://youtu.be/',
        r'https://www.youtube.com/watch\?v=',
        r'https://www.youtube.com/shorts/',
        r'https://youtube.com/shorts/'
    ]):
        youtube_video_handler(msg, bot)
    elif user_message_text == "↩️ Return" or user_message_text == "↩️ بازگشت":
        response = usermanager.return_response_based_on_language(persian=persian.returned_to_homepage)
        bot.send_message(chat_id, response, reply_markup=keyboardgenerator.homepage_buttons())
        for field in ["selecting_language", "joined_in_settings", "redeeming_code", "joined_in_support"]:
            users_collection.update_one({"_id": the_user["_id"]}, {"$set": {"metadata." + field: False}})
    elif user_message_text == "🛒 Buy Subscription" or user_message_text == "🛒 خرید اشتراک":
        if usermanager.get_user_language() == "en":
            bot.reply_to(msg, "Currently not available, You can use the bot with the free subscription.")
        else:
            bot.reply_to(msg, "در حال حاضر در دسترس نیست، می توانید با اشتراک رایگان از ربات استفاده کنید.")
    elif user_message_text == "👤 حساب کاربری" or user_message_text == "👤 Account":
        show_account(msg, bot)
    elif user_message_text == "📋 My Subscription" or user_message_text == "📋 اشتراک من":
        show_user_subscription_details(msg, bot)
    elif user_message_text == "🎁 کد هدیه" or user_message_text == "🎁 Gift Code":
        response = usermanager.return_response_based_on_language(persian=persian.send_the_giftcode)
        bot.send_message(chat_id, response, reply_markup=keyboardgenerator.return_buttons())
        users_collection.update_one(filter={"_id": the_user["_id"]}, update={"$set": {"metadata.redeeming_code": True}})
    elif user_message_text == "📖 Guide" or user_message_text == "📖 راهنما":
        response = usermanager.return_response_based_on_language(persian=persian.guide)
        bot.send_message(chat_id, response, parse_mode="Markdown")
    elif user_message_text == "⚙️ تنظیمات" or user_message_text == "⚙️ Settings":
        join_in_settings(msg, bot)
    elif user_message_text == "📞 پشتیبانی" or user_message_text == "📞 Support":
        join_in_support(msg, bot)
    elif the_user['metadata']["redeeming_code"] == True:
        redeem_giftcode(msg, bot)
    elif the_user['metadata']["joined_in_settings"] == True:
        if user_message_text == "🌐 Change Language" or user_message_text == "🌐 تغییر زبان":
            join_in_selecting_lang(msg, bot)
            users_collection.update_one(filter={"_id": the_user["_id"]},
                                        update={"$set": {"metadata.joined_in_settings": False}})
        else:
            response = usermanager.return_response_based_on_language(persian=persian.unknown_request)
            bot.reply_to(msg, response)
    elif the_user['metadata']["selecting_language"] == True:
        if user_message_text == "🇮🇷فارسی":
            selected_lang_is_fa(msg, bot)
        elif user_message_text == "🇺🇸English":
            selected_lang_is_en(msg, bot)
        else:
            bot.reply_to(msg,
                         f"ببخشید ولی منظورتان را متوجه نشدم🧐 لطفا از دکمه های زیر استفاده کنید👇\nSorry i didn't get what you mean🧐, please user the buttons below👇.")
    elif the_user['metadata']["joined_in_support"] == True:
        send_user_msg_to_support(msg, bot)
    elif usermanager.get_user_language() == "not_selected":
        the_user['metadata']["selecting_language"] = True
        bot.reply_to(msg, f"{persian.restart_required}\n\n{english.restart}")
    else:
        usermanager.return_response_based_on_language(persian=persian.unknown_request)
        bot.reply_to(msg, response)


def handle_user_photo(msg: telebot.types.Message, bot: telebot.TeleBot):
    the_user = users_collection.find_one({"user_id": msg.from_user.id})
    chat_id = msg.chat.id
    support_group_id = -4043182903
    if chat_id == support_group_id and msg.reply_to_message:
        reply_to_user_support_msg(msg, bot)
    if the_user['metadata']["joined_in_support"] == True:
        send_user_photo_to_support(msg, bot)
