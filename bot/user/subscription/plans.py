from jdatetime import datetime
class Plans:
    """
    premium plans
    """
    discount_percent = 20
    id_1_price = 48000
    id_2_price = 118000
    id_1_final_price = id_1_price * discount_percent // 100
    id_1_final_price = id_1_price - id_1_final_price
    id_2_final_price = id_2_price * discount_percent // 100
    id_2_final_price = id_2_price - id_2_final_price
    def _get_plan_by_id(self, plan_id):
        for plan in self.plans:
            plan_id = int(plan_id)
            if plan.get("id") == plan_id:
                return plan
    # download_links_last = 1 means 1 Hour
    plans = [
        {
            "id": 0,
            "type": "free",
            "max_file_size": 200,
            "max_data_per_day": 500,
            "used_data": 0,
            "remaining_data": 500,
            "quality_limit": "720p",
            "ads": True,
            "download_links_last": 1,
            "last_reset_date": datetime.today().strftime("%Y-%m-%d"),
        },
        {
            "id": 1,
            "type": "premium",
            "price": id_1_price,
            "discount_percent": discount_percent,
            "final_price": id_1_final_price,
            "days": 30,
            "days_left": 30,
            "max_file_size": 2000,
            "max_data_per_day": 40000,
            "used_data": 0,
            "remaining_data": 40000,
            "quality_limit": "1080p",
            "ads": False,
            "download_links_last": 24,
            "last_reset_date": datetime.today().strftime("%Y-%m-%d"),
        },
        {
            "id": 2,
            "type": "premium",
            "price": id_2_price,
            "discount_percent": discount_percent,
            "final_price": id_2_final_price,
            "days": 90,
            "days_left": 90,
            "max_file_size": 2000,
            "max_data_per_day": 40000,
            "used_data": 0,
            "remaining_data": 40000,
            "quality_limit": "1080p",
            "ads": False,
            "download_links_last": 24,
            "last_reset_date": datetime.today().strftime("%Y-%m-%d"),
        }
    ]