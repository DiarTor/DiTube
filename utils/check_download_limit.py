def file_size_exceeded(user_data, file_size):
    max_download_limit_per_file = user_data["subscription"]["max_size_per_file"]
    if file_size > max_download_limit_per_file:
        print(file_size)
        return False
    return True


def monthly_file_size_exceeded(user_data, file_size):
    remaining_size_available = user_data["subscription"]["remaining_size"]
    if file_size > remaining_size_available:
        return False
    return True
