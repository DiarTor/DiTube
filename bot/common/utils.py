import datetime
import time

from config.database import users_collection


def replace_invalid_characters_with_underscore(input_string: str) -> str:
    """
    Replace invalid characters with underscore in a string.
    :param input_string: The string you want to be processed.
    :return: The processed string.
    """
    invalid_characters = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_characters:
        input_string = input_string.replace(char, '_')

    return input_string


def reset_daily_data():
    """
    Reset daily data for users.
    Works every 24 hours.
    """
    while True:
        current_date = datetime.date.today().strftime("%Y-%m-%d")
        users = users_collection.find({"subscription.last_reset_date": {"$ne": current_date}})

        for user in users:
            daily_limit = user['subscription']['max_data_per_day']

            result = users_collection.update_one(
                {'_id': user['_id']},
                {"$set": {
                    "subscription.used_data": 0,
                    "subscription.remaining_data": daily_limit,
                    "subscription.last_reset_date": current_date
                }}
            )

            print(f"Matched: {result.matched_count}, Modified: {result.modified_count}")

        time.sleep(86400)
