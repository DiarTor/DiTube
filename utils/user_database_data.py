from bot.database import users_collection
async def change_user_subscription_size(user, filesize):
    existing_used_size = user["subscription"]["used_size"]
    existing_remaining_size = user["subscription"]["remaining_size"]
    monthly_limit = user["subscription"]["max_size_per_month"]
    new_used_size = existing_used_size + filesize
    new_remaining_size = existing_remaining_size - filesize
    users_collection.update_one(user, {
        "$set": {"subscription.used_size": new_used_size, "subscription.remaining_size": new_remaining_size}})