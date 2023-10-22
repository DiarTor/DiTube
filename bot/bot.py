from bot.config import TOKEN
from bot.handlers import start_handler, message_handler, callback_handler
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start_handler.start))
    application.add_handler((CallbackQueryHandler(callback_handler.handle_callback)))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler.handle_user_message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
