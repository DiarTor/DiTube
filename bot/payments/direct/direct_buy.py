from bot.user.subscription.plans import Plans
from config.database import users_collection


class DirectBuy:
    def __init__(self):
        self.users = users_collection

    def successful_payment(self, user_id: int,
                           plan_id: int = None):
        user = self.users.find_one({'user_id': user_id})
        plan = Plans()._get_plan_by_id(plan_id)
        if user:
            self.users.update_one({'user_id': user_id},
                                  {'$set': {'subscription': plan}})
