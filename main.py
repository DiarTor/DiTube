import logging

from pymongo import MongoClient
from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram import Update
from telegram.error import BadRequest
from telegram.ext import Application, CommandHandler, ContextTypes, filters, MessageHandler

from config import TOKEN
from langs import persian, english

# region logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
# endregion
# region database
client = MongoClient("mongodb://localhost:27017/")
db = client['jimoservice_db']
users_collection = db['users']
# endregion
select_lang_buttons = [
    [KeyboardButton("🇮🇷فارسی")],
    [KeyboardButton("🇺🇸English")]
]
select_lang_buttons_reply_markup = ReplyKeyboardMarkup(select_lang_buttons, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_data = {"user_id": user.id,
                 "lang": "not_selected",
                 "is_staff": False,
                 "donated": 0}
    if not users_collection.find_one({"user_id": user.id}):
        users_collection.insert_one(user_data)
    elif users_collection.find_one({"user_id": user.id})["lang"] == "not_selected":
        await Lang().join_in_selecting_lang(update, context)
    elif users_collection.find_one({"user_id": user.id})["lang"] == "en":
        await update.message.reply_text(f"{english.greeting}")
    elif users_collection.find_one({"user_id": user.id})["lang"] == "fa":
        await update.message.reply_text(f"{persian.greeting}")


async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    support_channel_id = -925489226
    chat_id = update.effective_chat.id
    user_message = update.message
    user_message_text = update.message.text
    user_reply = update.message.reply_to_message
    user_photo = update.message.photo
    user = update.effective_user
    if not users_collection.find_one({"user_id": user.id}):
        await update.message.reply_text(f"{persian.restart}\n\n{english.restart}")
        return
    elif context.user_data.get('selecting_lang'):
        if user_message_text == "🇮🇷فارسی":
            await Lang().selected_lang_is_fa(update, context)
        elif user_message_text == "🇺🇸English":
            await Lang().selected_lang_is_en(update, context)
        else:
            await update.message.reply_text(
                f"ببخشید ولی منظورتان را متوجه نشدم🧐 لطفا از دکمه های زیر استفاده کنید👇\nSorry i didn't get what you mean, please select the buttons below.")
    elif users_collection.find_one({"user_id": user.id})["lang"] == "not_selected":
        context.user_data['selecting_lang'] = True
        await update.message.reply_text(f"{persian.restart}\n\n{english.restart}")
    else:
        user_lang = users_collection.find_one({"user_id": user.id})["lang"]
        response = persian.didnt_understand if user_lang == "fa" else english.didnt_understand
        await update.message.reply_text(response)


class Lang:
    async def join_in_selecting_lang(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user
        if users_collection.find_one({"user_id": user.id})["lang"] == "not_selected":
            await update.message.reply_html(f"{persian.select_lang}\n\n{english.select_lang}",
                                            reply_markup=select_lang_buttons_reply_markup)
            context.user_data['selecting_lang'] = True
        elif users_collection.find_one({"user_id": user.id})["lang"] == "en":
            await update.message.reply_text(f"{english.select_lang}", reply_markup=select_lang_buttons_reply_markup)
            context.user_data['selecting_lang'] = True
        elif users_collection.find_one({"user_id": user.id})["lang"] == "fa":
            await update.message.reply_text(f"{persian.select_lang}", reply_markup=select_lang_buttons_reply_markup)
            context.user_data['selecting_lang'] = True

    async def selected_lang_is_fa(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user
        user_data = "fa"
        remove_markup = ReplyKeyboardRemove()
        users_collection.update_one({"user_id": user.id}, {"$set": {"lang": user_data}})
        await update.message.reply_text(f"{persian.greeting}", reply_markup=remove_markup)
        context.user_data["selecting_lang"] = False

    async def selected_lang_is_en(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user
        user_data = "en"
        remove_markup = ReplyKeyboardRemove()
        users_collection.update_one({"user_id": user.id}, {"$set": {"lang": user_data}})
        await update.message.reply_text(f"{english.greeting}", reply_markup=remove_markup)
        context.user_data["selecting_lang"] = False


class Staff:
    async def send(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not users_collection.find_one({"is_staff": True, "user_id": update.effective_user.id}):
            await update.message.reply_text("❌شما دسترسی به این دستور را ندارید.")
            return
        try:
            if context.args and context.args[0].isdigit() and context.args[1:]:
                user_id = int(context.args[0])
                message = " ".join(context.args[1:])
                await context.bot.send_message(user_id, f"👤یک پیام از مدیریت :\n\n{message}")
                await update.message.reply_text("✅پیام شما ارسال شد.")
            else:
                await update.message.reply_text("Usage: /send <user_id> <message>")
        except BadRequest:
            await update.message.reply_text("❌کاربر یافت نشد!")

    async def sendall(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not users_collection.find_one({"is_staff": True, "user_id": update.effective_user.id}):
            await update.message.reply_text("❌شما دسترسی به این دستور را ندارید.")
            return
        if context.args and context.args[0:]:
            documents = users_collection.find()
            message = " ".join(context.args[0:])
            for doc in documents:
                chat_id = doc['user_id']
                await context.bot.send_message(chat_id=chat_id, text=message)
            await update.message.reply_text("✅پیام شما ارسال شد.")
        else:
            await update.message.reply_text("Usage: /sendall <message>")

    async def ahelp(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not users_collection.find_one({"is_staff": True, "user_id": update.effective_user.id}):
            await update.message.reply_text("❌شما دسترسی به این دستور را ندارید.")
            return
        await update.message.reply_text("/send - Send message to a user\n/sendall - Send message to all users")


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("lang", Lang().join_in_selecting_lang))
    application.add_handler(CommandHandler("send", Staff().send))
    application.add_handler(CommandHandler("sendall", Staff().sendall))
    application.add_handler(CommandHandler("ahelp", Staff().ahelp))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
