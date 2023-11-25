import datetime
class Plans:
    discount_percent = 20
    premiun_30_price = 48000
    premiun_60_price = 78000
    premiun_30_final_price = premiun_30_price * discount_percent // 100 - premiun_30_price
    premiun_60_final_price = premiun_60_price * discount_percent // 100 - premiun_60_price

    # download_links_last = 1 means 1 Hour
    free = {
        "type": "free",
        "max_file_size": 200,
        "max_data_per_day": 500,
        "used_data": 0,
        "remaining_data": 500,
        "quality_limit": "720p",
        "ads": True,
        "download_links_last": 1,
        "last_reset_date": datetime.date.today().strftime("%Y-%m-%d"),

    }
    premium_30 = {
        "type": "premium",
        "price": premiun_30_price,
        "discount_percent": discount_percent,
        "final_price": premiun_30_final_price,
        "days": 30,
        "days_left": 30,
        "max_file_size": 2000,
        "max_data_per_day": 40000,
        "used_data": 0,
        "remaining_data": 40000,
        "quality_limit": "1080p",
        "ads": False,
        "download_links_last": 24,
        "last_reset_date": datetime.date.today().strftime("%Y-%m-%d"),
    }
    premium_60 = {
        "type": "premium",
        "price": premiun_60_price,
        "discount_percent": discount_percent,
        "final_price": premiun_60_final_price,
        "days": 60,
        "days_left": 60,
        "max_file_size": 2000,
        "max_data_per_day": 40000,
        "used_data": 0,
        "remaining_data": 40000,
        "quality_limit": "1080p",
        "ads": False,
        "download_links_last": 24,
        "last_reset_date": datetime.date.today().strftime("%Y-%m-%d"),
    }