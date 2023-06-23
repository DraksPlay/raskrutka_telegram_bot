import json
import time
import requests
import hashlib
import hmac

merchant_id = "23384"
currency = "RUB"


def create_form(order_amount, order_id):
    hash_text = merchant_id + ":" + str(order_amount) + ":" + "m7ioRpwCHrZt[+v" + ":" + currency + ":" + str(order_id)
    sign = hashlib.md5(hash_text.encode()).hexdigest()
    return f"https://pay.freekassa.ru/?m={merchant_id}&oa={order_amount}&currency={currency}&o={order_id}&s={sign}"


def get_order():
    data = {
        "shopId": merchant_id,
        "nonce": str(time.time()),
    }
    data = dict(sorted(data.items()))
    implode = "|".join(list(data.values()))
    sign = hmac.new(b"01f8e9b7116074c00a52d38391acbdb3", implode.encode(), digestmod=hashlib.sha256).hexdigest()
    data["signature"] = sign
    r = requests.get("https://api.freekassa.ru/v1/orders", data=json.dumps(data))
    return r.json()

