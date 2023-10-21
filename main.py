import logging
import threading

from bot import bot
from utils.modify_user_data import reset_daily_data

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    reset_thread = threading.Thread(target=reset_daily_data)
    reset_thread.start()
    bot.main()
