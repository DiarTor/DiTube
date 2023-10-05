from telegram import Update
from telegram.ext import ContextTypes


async def check_sub(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id):
    channel_id = -1001594818741
    try:
        chat_member = await context.bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        if chat_member.status in ["member", "administrator", "creator"]:
            return True
    except Exception as e:
        print(str(e))
    return False
