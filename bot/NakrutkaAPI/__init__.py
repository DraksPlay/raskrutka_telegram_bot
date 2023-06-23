import requests


class Nakrutka:

    def __init__(self, api_key):
        self.url = "https://nakruti.net/api/v2"
        self.api_key = api_key

    def get_balance(self):
        r = requests.post(self.url, params={"key": self.api_key, "action": "balance"})
        return r.json()

    def add_order(self, service, link, quantity):
        r = requests.post(self.url, params={"key": self.api_key, "action": "add", "service": service,
                                            "link": link, "quantity": quantity})
        return r.json()

    def order_status(self, order):
        r = requests.post(self.url, params={"key": self.api_key, "action": "status", "order": order})
        return r.json()

    def order_statuses(self, orders: str):
        r = requests.post(self.url, params={"key": self.api_key, "action": "status", "orders": orders})
        return r.json()
