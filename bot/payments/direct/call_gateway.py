from bot.user.subscription.plans import Plans
from languages import persian
from zibal_gateway import send_request


class CallGateway:

    def _generate_link(self, track_id):
        link = f"https://gateway.zibal.ir/start/{track_id}"
        return link

    def send_gateway_link(self, msg, bot, link):
        bot.send_message(msg.chat.id, persian.payment_gateway_generated.format(link))

    def process(self, msg, bot, plan_id, user_id):
        plan = Plans()._get_plan_by_id(plan_id)
        plan_price = plan['final_price']
        plan_price = plan_price * 10
        response = send_request(amount=plan_price, order_id=f"{plan_id}-{user_id}", description=plan.get('description'))
        track_id = response.get('trackId')
        link = self._generate_link(track_id)
        self.send_gateway_link(msg=msg, bot=bot, link=link)
