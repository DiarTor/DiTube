from telegram import ReplyKeyboardMarkup
from telegram import Update
from telegram.ext import ContextTypes
from utils.buttons import settings_buttons
from utils.check_user_data import get_user_lang


async def join_in_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    context.user_data["joined_in_settings"] = True
    user_lang = get_user_lang(user.id)
    response = "Please Use The Buttons Below " if user_lang == "en" else "لطفا از دکمه های زیر استفاده کنید"
    await update.message.reply_text(response,
                                    reply_markup=ReplyKeyboardMarkup(settings_buttons(user.id), resize_keyboard=True))
