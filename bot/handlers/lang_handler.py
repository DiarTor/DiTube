from bot.database import users_collection
from langs import persian, english
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram import Update
from telegram.ext import ContextTypes

select_lang_buttons = [
    [KeyboardButton("🇺🇸English"), KeyboardButton("🇮🇷فارسی")]
]
select_lang_buttons_reply_markup = ReplyKeyboardMarkup(select_lang_buttons, resize_keyboard=True)


async def join_in_selecting_lang(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_lang = users_collection.find_one({"user_id": user.id})["settings"]["language"]
    if user_lang == "not_selected":
        await update.message.reply_html(f"{persian.select_lang}\n\n{english.select_lang}",
                                        reply_markup=select_lang_buttons_reply_markup)
        context.user_data['selecting_lang'] = True
    elif user_lang == "en":
        await update.message.reply_text(f"{english.change_lang}", reply_markup=select_lang_buttons_reply_markup)
        context.user_data['selecting_lang'] = True
    elif user_lang == "fa":
        await update.message.reply_text(f"{persian.change_lang}", reply_markup=select_lang_buttons_reply_markup)
        context.user_data['selecting_lang'] = True


async def selected_lang_is_fa(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_data = "fa"
    remove_markup = ReplyKeyboardRemove()
    users_collection.update_one({"user_id": user.id}, {"$set": {"settings.language": user_data}})
    await update.message.reply_text(f"{persian.lang_changed}", reply_markup=remove_markup)
    context.user_data["selecting_lang"] = False


async def selected_lang_is_en(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_data = "en"
    remove_markup = ReplyKeyboardRemove()
    users_collection.update_one({"user_id": user.id}, {"$set": {"settings.language": user_data}})
    await update.message.reply_text(f"{english.lang_changed}", reply_markup=remove_markup)
    context.user_data["selecting_lang"] = False
