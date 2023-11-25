import datetime
import time

from bot.user_management.subscription.plans import Plans
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


def modify_daily_data(interval_in_seconds=86400):
    """
    Modify daily data for premium users at a specified interval.

    :param interval_in_seconds: The interval between modifications (default is 24 hours).
    """
    while True:
        try:
            current_date = datetime.date.today().strftime("%Y-%m-%d")
            users = users_collection.find({"subscription.last_reset_date": {"$ne": current_date}})

            for user in users:
                daily_limit = user['subscription']['max_data_per_day']
                if user['subscription']['type'] != 'free':
                    subscription_days_left = user['subscription']['days_left']

                    # Ensure 'days_left' doesn't go below zero
                    new_days_left = max(subscription_days_left - 1, 0)

                    result = users_collection.update_one(
                        {'_id': user['_id']},
                        {"$set": {
                            "subscription.days_left": new_days_left,
                            "subscription.used_data": 0,
                            "subscription.remaining_data": daily_limit,
                            "subscription.last_reset_date": current_date
                        }}
                    )

                    print(
                        f"User: {user['_id']}, Days Left: {new_days_left}, Matched: {result.matched_count}, Modified: {result.modified_count}")
                    if new_days_left == 0:
                        users_collection.update_one(
                            {'_id': user['_id']},
                            {"$set": {"subscription": Plans().free}}
                        )
                elif user['subscription']['type'] == 'free':
                    users_collection.update_one(
                        {'_id': user['_id']},
                        {"$set": {
                            "subscription.used_data": 0,
                            "subscription.remaining_data": daily_limit,
                            "subscription.last_reset_date": current_date
                        }}
                    )

            time.sleep(interval_in_seconds)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
