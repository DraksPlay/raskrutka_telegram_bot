def orders_handler():
    import time
    import bot.database as database
    import configparser
    from . import Nakrutka
    import os
    config = configparser.ConfigParser()
    config.read(os.getcwd() + "/bot/config.ini")

    db = database.Database(host=config["Database"]["host"],
                         user=config["Database"]["user"],
                         password=config["Database"]["password"],
                         name=config["Database"]["name"],
                           debug=int(config["Bot"]["debug"]))

    nakrutka = Nakrutka(config["NakrutkaAPI"]["api_key"])

    while True:

        try:

            data_orders = db.orders.all()

            for order in data_orders:
                pass
            time.sleep(2)
        except KeyboardInterrupt:
            import sys
            sys.exit()