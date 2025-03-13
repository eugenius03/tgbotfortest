from liqpay import LiqPay
import pytz
from datetime import datetime
from os import getenv
from dotenv import load_dotenv
import logging
import requests

class Payment:
    def __init__ (self):
        load_dotenv()
        self.LIQ_PUBLIC = getenv("LIQ_PUBLIC")
        LIQ_PRIVATE = getenv("LIQ_PRIVATE")
        self.liqpay = LiqPay(self.LIQ_PUBLIC, LIQ_PRIVATE)
        self.data = {
            "version": 3,
            "public_key": self.LIQ_PUBLIC,
        }

    async def generate_url(self, order_id, amount, description):
        data = {k: v for k, v in self.data.items()}
        # створення даних по поточному платежу
        data['action'] = "pay"
        data["amount"] = amount
        data["currency"] = "UAH"
        data["language"] = "uk"
        data["description"] = f"Оплата замовлення в боті. {description}"
        data["order_id"] = order_id
        data_to_sign = self.liqpay.data_to_sign(data)
        params = {'data': data_to_sign,
                  'signature': self.liqpay.cnb_signature(data)}
        res = None

        try:
            res = requests.post(url='https://www.liqpay.ua/api/3/checkout/', data=params)
            if res.status_code == 200:
                print("+")
                return res.url
            else:
                logging.warning(f"time {datetime.now(pytz.timezone('Europe/Kiev'))}| incorrect status code form response - {res.status_code}, must be 200, "
                                f"data- {data}, params - {params}")
                return
        except:
            logging.exception(f'error getting response from liqpay, '
                              f'res - {res}, data- {data}, params - {params}')
            
    def get_order_status(self, order_id):
        data = {k: v for k, v in self.data.items()}
        data["action"] = "status"
        data["order_id"] = order_id
        res = self.liqpay.api("request", data)
        if res.get("action") == "pay":
            if res.get('public_key') == self.LIQ_PUBLIC:
                return res
        return False
    
payment = Payment()