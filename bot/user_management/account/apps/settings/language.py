import telebot.types
from bot.user_management.utils.button_utils import KeyboardMarkupGenerator
from config.database import users_collection
from languages import persian, english
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

select_lang_buttons = [[KeyboardButton("🇺🇸English"), KeyboardButton("🇮🇷فارسی")]]
select_lang_buttons_reply_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
for row in select_lang_buttons:
    select_lang_buttons_reply_markup.row(*row)


def join_in_selecting_lang(msg: telebot.types.Message, bot: telebot.TeleBot):
    user = msg.from_user
    the_user = users_collection.find_one({"user_id": user.id})
    filter = {"_id": the_user["_id"]}
    user_lang = the_user["settings"]["language"]
    if user_lang == "not_selected":
        bot.send_message(msg.chat.id, f"{persian.starting_select_lang}\n\n{english.starting_select_lang}",
                         reply_markup=select_lang_buttons_reply_markup)
        users_collection.update_one(filter=filter, update={"$set": {"metadata.selecting_language": True}})
    elif user_lang == "en":
        bot.send_message(msg.chat.id, english.change_language, reply_markup=select_lang_buttons_reply_markup)
        users_collection.update_one(filter=filter, update={"$set": {"metadata.selecting_language": True}})
    elif user_lang == "fa":
        bot.send_message(msg.chat.id, persian.change_language, reply_markup=select_lang_buttons_reply_markup)
        users_collection.update_one(filter=filter, update={"$set": {"metadata.selecting_language": True}})


def selected_lang_is_fa(msg: telebot.types.Message, bot: telebot.TeleBot):
    user = msg.from_user
    the_user = users_collection.find_one({"user_id": user.id})
    users_collection.update_one({"_id": the_user["_id"]}, {"$set": {"settings.language": "fa"}})
    bot.send_message(msg.chat.id, persian.language_changed,
                     reply_markup=KeyboardMarkupGenerator(user.id).homepage_buttons())
    users_collection.update_one(filter={"_id": the_user["_id"]},
                                update={"$set": {"metadata.selecting_language": False}})


def selected_lang_is_en(msg: telebot.types.Message, bot: telebot.TeleBot):
    user = msg.from_user
    the_user = users_collection.find_one({"user_id": user.id})
    users_collection.update_one({"_id": the_user["_id"]}, {"$set": {"settings.language": "en"}})
    bot.send_message(msg.chat.id, english.language_changed,
                     reply_markup=KeyboardMarkupGenerator(user.id).homepage_buttons())
    users_collection.update_one(filter={"_id": the_user["_id"]},
                                update={"$set": {"metadata.selecting_language": False}})
