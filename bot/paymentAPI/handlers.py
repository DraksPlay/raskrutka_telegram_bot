

def orders_handler():
    while True:
        try:
            import time
            import bot.database as database
            import configparser
            import bot.paymentAPI.paymentQIWI as payment
            import os
            config = configparser.ConfigParser()
            config.read(os.getcwd() + "/bot/config.ini")

            db = database.Database(host=config["Database"]["host"],
                                 user=config["Database"]["user"],
                                 password=config["Database"]["password"],
                                 name=config["Database"]["name"],
                                 debug=int(config["Bot"]["debug"]))

            while True:
                data_orders = db.form_payment.all()

                for order in data_orders:
                    data = payment.get_order(order["billId"])

                    if "status" in data:
                        if data["status"]["value"] == "PAID":
                            db.users.user_save("balance", int(db.users.user_read(order["user_id"])["balance"]) + round(float(order["amount"]) * 100), order["user_id"])
                            db.form_payment.delete(data["billId"])
                        elif data["status"]["value"] != "WAITING":
                            db.form_payment.delete(data["billId"])
                    else:
                        db.form_payment.delete(order["billId"])
                time.sleep(2)
        except KeyboardInterrupt:
            import sys
            sys.exit()
        except Exception as exc:
            continue