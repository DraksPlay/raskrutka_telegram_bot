import sys
import time


def main():
    if len(sys.argv) > 1:
        if "runbot" in sys.argv:
            print("Запуск бота...")
            import multiprocessing
            from bot import bot
            import bot.paymentAPI.handlers as handlers_payment
            import bot.NakrutkaAPI.handlers as handlers_nakrutka

            bot_process = multiprocessing.Process(target=bot.main)
            handler_payment_process = multiprocessing.Process(target=handlers_payment.orders_handler)
            handler_nakrutka_process = multiprocessing.Process(target=handlers_nakrutka.orders_handler)
            bot_process.start()
            handler_payment_process.start()
            handler_nakrutka_process.start()

            time.sleep(0.1)
            while True:
                response = input("[me]: ")
                if response == "/exit":
                    bot_process.terminate()
                    handler_nakrutka_process.terminate()
                    handler_payment_process.terminate()
                    print("end")
                    break

        else:
            raise "Не было найдено аргументов по управлению ботом! Передайте аргумент help, для получения списка команд."
    else:
        raise "Не было передано аргументов по управлению ботом! Передайте аргумент help, для получения списка команд."


if __name__ == '__main__':
    main()