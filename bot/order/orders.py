order_progress = {0: {"text": "‼Убедитесь, что Ваш профиль открыт, иначе услуга будет отменена\n🎯 Сервис: {}\n🚨 Услуга: {}\n📉 Минимум: {}\n📈 Максимум: {}\n💵 Цена за 1000: {} ₽\n\n✏ Введите кол-во для накрутки:",
                      "format": ["platform", "name", "min", "max", "price"],
                      "conditions": ["min<=val<=max"]},
                  1: {"text": "‼Убедитесь, что ссылка корректна, иначе услуга будет отменена\n💻 Введите ссылку для накрутки:",
                      "conditions": ["short_512"]}}


def get_text(user_data, service_id=None):
    number_order_progress = len(user_data["create_order"].split("\n"))-1
    service: dict
    with open("bot/order/services.json", "r", encoding="utf-8") as file:
        import json
        service = json.load(file)
        file.close()
    if number_order_progress == len(order_progress):
        return "!end"
    res = order_progress[number_order_progress]["text"]
    if service_id:
        if service_id in service:
            service = service[service_id]
            from bot.balance import convert_str_to_money
            service["price"] = convert_str_to_money(service["price"])
            if "format" in order_progress[number_order_progress]:
                args_to_format = [service[arg] for arg in order_progress[number_order_progress]["format"]]
                res = res.format(*args_to_format)
            return res
        else:
            return False
    else:
        return res


def check_conditions(user_data, user_message, service_id=None):
    number_order_progress = len(user_data["create_order"].split("\n")) - 1
    if number_order_progress in order_progress:
        if "conditions" in order_progress[number_order_progress]:
            service: dict
            with open("bot/order/services.json", "r") as file:
                import json
                service = json.load(file)
                file.close()
            for cond in order_progress[number_order_progress]["conditions"]:
                if cond == "min<=val<=max":
                    service = service[service_id]
                    if user_message.isnumeric():
                        if service["min"] <= int(user_message) <= service["max"]:
                            return (True, "")
                        else:
                            return (False, "❌ Значение должно находиться в диапазоне!")
                    else:
                        return (False, "❌ Значение должно быть целым числом!")
                if cond == "short_512":
                    if len(user_message) <= 512:
                        return (True, "")
                    else:
                        return (False, "❌ Ссылка должна быть не больше 512 символов (сейчас: {})!".format(len(user_message)))
            else:
                return (True, "")
        else:
            return (True, "")
    else:
        return (False, "❌ Ошибка заполнения заказа!")
