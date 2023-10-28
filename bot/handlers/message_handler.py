import re

import telebot.types
from bot.database import users_collection
from bot.handlers.yt_link_handler import youtube_video_handler, youtube_shorts_handler
from bot.users.account.account import show_account
from bot.users.giftcode.giftcode import redeem_giftcode
from bot.users.my_subscription.my_subscription import show_user_subscription_details
from bot.users.settings.language import join_in_selecting_lang
from bot.users.settings.language import selected_lang_is_en, selected_lang_is_fa
from bot.users.settings.settings import join_in_settings
from langs import persian, english
from utils.buttons import homepage_buttons, return_buttons
from utils.get_user_data import get_user_lang
from utils.is_channel_sub import check_sub


def handle_user_message(msg: telebot.types.Message, bot: telebot.TeleBot):
    user = msg.from_user
    the_user = users_collection.find_one({"user_id": user.id})
    chat_id = msg.chat.id
    user_message = msg
    user_message_text = msg.text
    user_photo = msg.photo
    user_reply = msg.reply_to_message
    support_channel_id = -925489226
    if not check_sub(msg, bot):
        bot.reply_to(msg, f"Please subscribe and then use /start.\n @diardev")
        return
    elif not users_collection.find_one({"user_id": user.id}):
        bot.reply_to(msg, f"{persian.restart}\n\n{english.restart}")
        return
    elif re.search(r'https://youtu.be/|https://www.youtube.com/watch\?v=', user_message_text):
        youtube_video_handler(msg, bot)
    elif re.search(r"https://youtube.com/shorts/", user_message_text):
        youtube_shorts_handler(msg, bot)
    elif user_message_text == "↩️ Return" or user_message_text == "↩️ بازگشت":
        user_lang = get_user_lang(user_id=user.id)
        response = "Returned to the main menu" if user_lang == "en" else "بازگشت به صفحه اصلی"
        bot.send_message(chat_id, response, reply_markup=homepage_buttons(user.id))
        for field in ["selecting_language", "joined_in_settings", "redeeming_code"]:
            users_collection.update_one({"_id": the_user["_id"]}, {"$set": {"metadata." + field: False}})
    elif user_message_text == "👤 حساب کاربری" or user_message_text == "👤 Account":
        show_account(msg, bot)
    elif user_message_text == "📋 My Subscription" or user_message_text == "📋 اشتراک من":
        show_user_subscription_details(msg, bot)
    elif user_message_text == "🎁 کد هدیه" or user_message_text == "🎁 Gift Code":
        bot.send_message(chat_id, f"Now Send the code you want to redeem", reply_markup=return_buttons(user.id))
        users_collection.update_one(filter={"_id": the_user["_id"]}, update={"$set": {"metadata.redeeming_code": True}})
    elif user_message_text == "📖 Guide" or user_message_text == "📖 راهنما":
        user_guide_text = """
        How to Use *MiTube*:
1. Send a YouTube video URL.
2. Choose the download Method.
3. Enjoy your downloaded video!
    
🌐@DiarDev
🤖@MiTubeRobot"""
        bot.send_message(chat_id, user_guide_text, parse_mode="Markdown")
    elif user_message_text == "⚙️ تنظیمات" or user_message_text == "⚙️ Settings":
        join_in_settings(msg, bot)
    elif the_user['metadata']["redeeming_code"] == True:
        redeem_giftcode(msg, bot)
    elif the_user['metadata']["joined_in_settings"] == True:
        if user_message_text == "🌐 Change Language" or user_message_text == "🌐 تغییر زبان":
            join_in_selecting_lang(msg, bot)
            users_collection.update_one(filter={"_id": the_user["_id"]},
                                        update={"$set": {"metadata.joined_in_settings": False}})
        else:
            user_lang = get_user_lang(user_id=user.id)
            response = persian.didnt_understand if user_lang == "fa" else english.didnt_understand
            bot.reply_to(msg, response)
    elif the_user['metadata']["selecting_language"] == True:
        if user_message_text == "🇮🇷فارسی":
            selected_lang_is_fa(msg, bot)
        elif user_message_text == "🇺🇸English":
            selected_lang_is_en(msg, bot)
        else:
            bot.reply_to(msg,
                         f"ببخشید ولی منظورتان را متوجه نشدم🧐 لطفا از دکمه های زیر استفاده کنید👇\nSorry i didn't get what you mean, please select the buttons below.")
    elif get_user_lang(user_id=user.id) == "not_selected":
        the_user['metadata']["selecting_language"] = True
        bot.reply_to(msg, f"{persian.restart}\n\n{english.restart}")
    else:
        user_lang = get_user_lang(user_id=user.id)
        response = persian.didnt_understand if user_lang == "fa" else english.didnt_understand
        bot.reply_to(msg, response)
