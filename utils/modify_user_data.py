import datetime
import time
from bot.database import users_collection


def change_user_subscription_size(user, filesize):
    existing_used_size = user["subscription"]["used_data"]
    existing_remaining_size = user["subscription"]["remaining_data"]
    monthly_limit = user["subscription"]["max_data_per_day"]
    new_used_data = existing_used_size + filesize
    new_remaining_data = existing_remaining_size - filesize
    filter = {"_id": user["_id"]}
    update = {"$set": {"subscription.used_data": new_used_data, "subscription.remaining_data": new_remaining_data}}
    users_collection.update_one(filter, update)


def reset_daily_data():
    while True:
        current_date = datetime.date.today().strftime("%Y-%m-%d")
        users = users_collection.find({"subscription.last_reset_date": {"$ne": current_date}})

        for user in users:
            daily_limit = user['subscription']['max_data_per_day']

            result = users_collection.update_one({'_id': user['_id']}, {
                "$set": {"subscription.used_data": 0, "subscription.remaining_data": daily_limit,
                    "subscription.last_reset_date": current_date}})

            print(f"Matched: {result.matched_count}, Modified: {result.modified_count}")

        time.sleep(86400)  # Sleep for 24 hours (86400 seconds)
