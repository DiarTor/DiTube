from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from bot.handlers import start_handler, lang_handler, staff_handler, help_handler, message_handler
from bot.config import TOKEN


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start_handler.start))
    application.add_handler(CommandHandler("lang", lang_handler.join_in_selecting_lang))
    application.add_handler(CommandHandler("help", help_handler.help))
    application.add_handler(CommandHandler("send", staff_handler.send))
    application.add_handler(CommandHandler("sendall", staff_handler.sendall))
    application.add_handler(CommandHandler("adminhelp", help_handler.adminhelp))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler.handle_user_message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
