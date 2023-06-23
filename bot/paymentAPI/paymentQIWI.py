import json
import time
import datetime
import requests


def get_order(bill_id):
    url = f"https://api.qiwi.com/partner/bill/v1/bills/{bill_id}"
    header = {
        "Accept": "application/json",
        "Authorization": "Bearer eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6InFkcnN2Yi0wMCIsInVzZXJfaWQiOiI3OTUwNjEyMjQwMyIsInNlY3JldCI6IjNiZGJiMjNkN2ZmNWYwMDBjOGU2ODg1OTQ4ZjhjNWMyZWYzNTAyMjE4YzQ4MzgyMDY0YmU4NzdlYWZiYjkwNWUifX0="
    }
    r = requests.get(url, headers=header)
    return r.json()


def create_order(amount):
    life_order = 1800
    bill_id = round(time.time())
    expiration_date_time = (datetime.datetime.now() + datetime.timedelta(seconds=life_order)).strftime("%Y-%m-%dT%H:%M:%S+03:00")
    url = f"https://api.qiwi.com/partner/bill/v1/bills/{bill_id}"
    header = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6InFkcnN2Yi0wMCIsInVzZXJfaWQiOiI3OTUwNjEyMjQwMyIsInNlY3JldCI6IjNiZGJiMjNkN2ZmNWYwMDBjOGU2ODg1OTQ4ZjhjNWMyZWYzNTAyMjE4YzQ4MzgyMDY0YmU4NzdlYWZiYjkwNWUifX0="
    }
    params = {
        "amount": {
         "currency": "RUB",
         "value": f"{amount}.00"
        },
        "comment": "Пополнение баланса",
        "expirationDateTime": expiration_date_time,
    }
    r = requests.put(url, headers=header, json=params)
    return r.json()


