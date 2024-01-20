import requests
from bot.payments.direct.direct_buy import DirectBuy
from flask import Flask, request
from config.token import MERCHANT_ID
import telebot
app = Flask(__name__)
merchant = 'zibal'
callback_url = "http://localhost:8000/verify-payment"


@app.route('/', methods=['GET'])
def homepage():
    return "Hi there"


def send_request(amount, order_id, mobile=None, description=None, multiplexingInfos=None):
    data = {}
    data['merchant'] = merchant
    data['callbackUrl'] = callback_url
    data['amount'] = amount

    data['orderId'] = order_id
    data['mobile'] = mobile
    data['description'] = description
    data['multiplexingInfos'] = multiplexingInfos

    response = post_to('request', data)
    return response


@app.route('/verify-payment', methods=['POST', 'GET'])
def check_payment():
    order_id = request.args.get('orderId')
    order_id_parts = order_id.split('-')
    plan_id = order_id_parts[0]
    user_id = order_id_parts[1]
    if request.args.get('success') == '1':
        trackId = request.args.get('trackId')
        result = verify(trackId)
        if result.get('result') == 100:
            try:
                DirectBuy().successful_payment(user_id=int(user_id), plan_id=plan_id)
            except Exception:
                return "payment error if your money didnt deposited in 48 hrs please contact support"
            return "success return to the bot"
        elif result.get('result') == 201:
            return "previously verifed"
        else:
            return "payment error"
        return "success"
    else:
        return "fail"


def inquiry(trackId):
    data = {}
    data['merchant'] = merchant
    data['trackId'] = trackId
    return post_to('inquiry', data)


def verify(trackId):
    data = {}
    data['merchant'] = merchant
    data['trackId'] = trackId
    return post_to('verify', data)


def post_to(path, parameters):
    url = "https://gateway.zibal.ir/v1/" + path

    response = requests.post(url=url, json=parameters)

    return response.json()


if __name__ == "__main__":
    app.run(debug=True, port=8000)
