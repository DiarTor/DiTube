import datetime

from bot.database import users_collection
from jdatetime import datetime as jdatetime


def get_user_lang(user_id):
    return users_collection.find_one({"user_id": user_id})["settings"]["language"]


def get_user_subscription_data(user_id):
    return users_collection.find_one({"user_id": user_id})["subscription"]

def get_user_lang_and_return_response(user_id, persian= None, english = None):
    user_lang = get_user_lang(user_id)
    response: str = english if user_lang == "en" else persian
    return response
