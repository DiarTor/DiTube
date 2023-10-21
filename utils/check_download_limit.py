def file_size_exceeded(user_data, file_size):
    max_file_size = user_data["subscription"]["max_file_size"]
    if file_size > max_file_size:
        return False
    return True


def daily_file_size_exceeded(user_data, file_size):
    remaining_size_available = user_data["subscription"]["remaining_data"]
    if file_size > remaining_size_available:
        return False
    return True
