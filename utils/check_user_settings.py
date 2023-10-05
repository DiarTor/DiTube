from bot.database import users_collection


def check_user_lang(user_id):
    return users_collection.find_one({"user_id": user_id})["settings"]["language"]
