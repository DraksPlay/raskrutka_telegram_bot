# -*- coding: utf-8 -*-



def main():
    import telebot
    from telebot import types
    import configparser
    import bot.database as database
    import bot.keyboards_templates as kt
    import bot.text_templates as tt
    from bot.balance import convert_str_to_money
    import bot.paymentAPI.paymentQIWI as payment
    from .NakrutkaAPI import Nakrutka
    import os
    import time
    import logging
    logging.basicConfig(filename="log.txt",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S')

    config = configparser.ConfigParser()
    config.read(os.getcwd()+"/bot/config.ini")
    print("Бот запущен!")
    try_count = 0

    while True:
        try:

            bot = telebot.TeleBot(token=config["Telegram"]["token"])
            db = database.Database(host=config["Database"]["host"],
                                   user=config["Database"]["user"],
                                   password=config["Database"]["password"],
                                   name=config["Database"]["name"],
                                   debug=int(config["Bot"]["debug"]))

            nakrutka = Nakrutka(config["NakrutkaAPI"]["api_key"])

            def save_message_user(user_id, message):
                import datetime
                try:
                    with open("messages.txt", "a", encoding="utf-8") as file:
                        file.write("[{}] {}: {}\n".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id, message))
                        file.close()
                except:
                    return 0

            def inline_keyboards(keyboards):
                markup = types.InlineKeyboardMarkup()
                for row in keyboards:
                    elems = []
                    for elem in row:
                        elems.append(types.InlineKeyboardButton(text=elem["text"],
                                                                callback_data=(elem["callback"] if "callback" in elem else None),
                                                                url=(elem["url"] if "url" in elem else None)))
                    markup.add(*elems)
                return markup

            @bot.callback_query_handler(func=lambda c: True)
            def callback_query(call):
                user_id = call.message.chat.id
                message_id = call.message.message_id
                user_data = db.users.user_read(user_id)
                call_data_split = call.data.split("/")
                save_message_user(str(user_id) + f" ({call.from_user.username})", call.data)
                if not user_data:
                    db.users.user_add(user_id)
                    user_data = db.users.user_read(user_id)
                if call_data_split[0] == "hub":
                    db.users.user_save("botpath", "", user_id)
                    bot.edit_message_text(tt.menu, user_id, message_id, reply_markup=inline_keyboards(kt.create_inline(kt.menu)))
                elif call_data_split[0] == "promote":
                    list_promote = {"telegram": kt.promote_telegram, "instagram": kt.promote_instagram, "vk": kt.promote_vk}
                    if len(call_data_split) == 1:
                        bot.edit_message_text(tt.promote, user_id, message_id, reply_markup=inline_keyboards(kt.create_inline(kt.promote, end=["hub"])))
                    elif call_data_split[1] in list_promote:
                        if len(call_data_split) == 2:
                            bot.edit_message_text(tt.service, user_id, message_id, reply_markup=inline_keyboards(kt.create_inline(list_promote[call_data_split[1]], end=["back", "hub"], call=call.data)))
                        else:
                            from bot.order import orders
                            service_id = call_data_split[1]+"/"+call_data_split[2]
                            db.users.user_save("create_order", service_id, user_id)
                            user_data["create_order"] = service_id
                            text = orders.get_text(user_data, service_id)
                            if text:
                                db.users.user_save("botpath", "create_order/fill", user_id)
                                bot.edit_message_text(text, user_id, message_id, reply_markup=inline_keyboards(kt.create_inline(end=["back", "hub"], call=call.data)))
                            else:
                                bot.edit_message_text("❌ Данной услуги не существует!", user_id, message_id, reply_markup=inline_keyboards(kt.hub))
                elif call_data_split[0] == "create_order":
                    if len(call_data_split) == 2:
                        if call_data_split[1] == "edit":
                            from bot.order import orders
                            service_id = user_data["create_order"].split('\n')[0]
                            db.users.user_save("create_order", service_id, user_id)
                            user_data["create_order"] = service_id
                            text = orders.get_text(user_data, service_id)
                            if text:
                                db.users.user_save("botpath", "create_order/fill", user_id)
                                bot.edit_message_text(text, user_id, message_id, reply_markup=inline_keyboards(kt.hub))
                            else:
                                bot.edit_message_text("❌ Данной услуги не существует!", user_id, message_id, reply_markup=inline_keyboards(kt.hub))
                        elif call_data_split[1] == "complete":
                            import bot.NakrutkaAPI.table_service_id as table_service_id
                            order_create_data = user_data["create_order"].split("\n")
                            if order_create_data[0] in table_service_id.table:
                                price = round(table_service_id.table[order_create_data[0]]["price"] * int(order_create_data[1]) / 1000)
                                if price <= user_data["balance"]:
                                    order_id = nakrutka.add_order(table_service_id.table[order_create_data[0]]["service_id"] if order_create_data[0] in table_service_id.table else "", order_create_data[2], order_create_data[1])
                                    if "error" in order_id:
                                        logging.error(order_id)
                                        bot.edit_message_text("❌ Произошла ошибка на стороне сервера!\nПопробуйте повоторить попытку позже!", user_id, message_id, reply_markup=inline_keyboards(kt.hub))
                                    else:
                                        db.users.user_save("balance", user_data["balance"]-price, user_id)
                                        db.orders.create(order_id["order"], user_id, order_create_data[0], order_create_data[2], price)
                                        bot.edit_message_text("🤩 Заказ отправлен в работу! 🤩\n"
                                                              "💡 Скоро он начнёт выполняться.", user_id, message_id, reply_markup=inline_keyboards(kt.hub))
                                    db.users.user_save("botpath", "", user_id)
                                else:
                                    bot.edit_message_text("❌ У Вас недостаточно средств на балансе ({} ₽/{} ₽)!\nПополните его и повторите попытку.".format(convert_str_to_money(user_data["balance"]), convert_str_to_money(price)), user_id, message_id, reply_markup=inline_keyboards(kt.hub))
                            else:
                                bot.edit_message_text("❌ Услуга не корректна!\nСообщите в тех.поддержку!", user_id, message_id, reply_markup=inline_keyboards(kt.hub))
                elif call_data_split[0] == "orders":
                    orders = db.orders.user_orders(user_id)
                    if len(orders) == 0:
                        bot.edit_message_text("🥺 У Вас ещё нет заказов по раскрутке!", user_id, message_id, reply_markup=inline_keyboards(kt.hub))
                    else:
                        orders.reverse()
                        import bot.NakrutkaAPI.table_service_id as table_service_id
                        res = "📔 Список заказов:\n\n"
                        current_page = 1 if len(call_data_split) == 1 else int(call_data_split[1])
                        max_orders_in_page = 5
                        num_pages = len(orders)//max_orders_in_page + (1 if len(orders)%max_orders_in_page != 0 else 0)
                        order_statuses = nakrutka.order_statuses(",".join([str(order["id"]) for order in orders[(current_page - 1) * max_orders_in_page:current_page * max_orders_in_page]])).values()
                        order_statuses = reversed(order_statuses)
                        for index, value in enumerate(order_statuses):
                            index += max_orders_in_page*(current_page-1)
                            if "error" not in value and value != "Incorrect request":
                                if value["status"] == "Canceled" and orders[index]['back_money'] == 0:
                                    db.users.user_save("balance", user_data["balance"]+orders[index]['price'], user_id)
                                    user_data["balance"] += orders[index]['price']
                                    db.orders.update(orders[index]['id'], "back_money", 1)
                                statuses = {"Pending": "Ожидает", "In progress": "Выполняется", "Canceled": "Отменён (Средства возвращены)",
                                            "Completed": "Выполнено"}
                                if value["status"] in statuses:
                                    value["status"] = statuses[value["status"]]
                                res += f"🆔 Номера заказа: {orders[index]['number']}\n" \
                                       f"🚨 Название: {table_service_id.table[orders[index]['name']]['name']}\n" \
                                       f"💰 Цена: {convert_str_to_money(orders[index]['price'])} ₽\n" \
                                       f"💻 Ссылка: {orders[index]['link'][:1024//max_orders_in_page]}\n" \
                                       f"💡 Статус: {value['status']}\n" \
                                       f"📈 Стартовое значение: {value['start_count']}\n" \
                                       f"📉 Остаток: {value['remains']}\n\n"
                        pager = [[]]
                        last_page = {"text": "◀ "+str(current_page-1), "callback": f"orders/{str(current_page-1)}"} if current_page != 1 else False
                        next_page = {"text": str(current_page+1)+" ▶", "callback": f"orders/{str(current_page+1)}"} if current_page != num_pages else False
                        if last_page:
                            pager[0].append(last_page)
                        if next_page:
                            pager[0].append(next_page)
                        bot.edit_message_text(res, user_id, message_id,reply_markup=inline_keyboards(kt.hub+pager))
                elif call_data_split[0] == "personal_account":
                    bot.edit_message_text(tt.personal_account.format(call.from_user.username, convert_str_to_money(str(user_data["balance"]))), user_id, message_id, reply_markup=inline_keyboards(kt.hub))
                elif call_data_split[0] == "balance":
                    bot.edit_message_text(tt.balance.format(convert_str_to_money(str(user_data["balance"]))), user_id, message_id, reply_markup=inline_keyboards(kt.hub))
                elif call_data_split[0] == "add_balance":
                    db.users.user_save("botpath", "add_balance", user_id)
                    bot.edit_message_text(tt.add_balance, user_id, message_id, reply_markup=inline_keyboards(kt.hub))
                elif call_data_split[0] == "tutorial":
                    bot.edit_message_text(tt.tutorial, user_id, message_id, reply_markup=inline_keyboards(kt.hub))
                elif call_data_split[0] == "support":
                    db.users.user_save("botpath", "support", user_id)
                    bot.edit_message_text("✏ Введите сообщение для отправки", user_id, message_id, reply_markup=inline_keyboards(kt.hub))
                elif call_data_split[0] == "free_view":
                    data_fw = db.free_view.read(user_id)
                    if not data_fw:
                        db.free_view.create(user_id)
                        data_fw = db.free_view.read(user_id)
                    if time.time()-data_fw["last_take"] >= 86400:
                        db.users.user_save("botpath", "free_view", user_id)
                        bot.edit_message_text("💻 Введите ссылку для накрутки просмотров в telegram", user_id, message_id, reply_markup=inline_keyboards(kt.hub))
                    else:
                        bot.edit_message_text("😢 К сожалению бесплатные просмотры можно получить раз в день!\n"
                                              "🤩 Не хотите ждать? Тогда в любой момент Вы можете заказать ❤‍🔥РАСКРУТКУ❤‍🔥!", user_id, message_id, reply_markup=inline_keyboards(kt.hub))
                elif call_data_split[0] == "free_followers":
                    bot.edit_message_text("🥹 Данный раздел находится в разработке и совсем скоро заработает!", user_id, message_id, reply_markup=inline_keyboards(kt.hub))

            @bot.message_handler(commands=['start'])
            def start_message(message):
                save_message_user(str(message.chat.id) + f" ({message.from_user.username})", message.text)
                db.users.user_add(message.chat.id)
                bot.send_message(message.chat.id, tt.start)
                bot.send_photo(message.chat.id, "https://t.me/top_raskrutka1/8")
                bot.send_message(message.chat.id, tt.menu, reply_markup=inline_keyboards(kt.menu))

            @bot.message_handler(content_types=['text'])
            def message_reply(message):
                user_message = message.text
                user_id = message.chat.id
                save_message_user(str(user_id)+f" ({message.from_user.username})", user_message)
                user_data = db.users.user_read(user_id)
                user_message_split = user_message.split(" ")
                if user_data:
                    user_data_botpath = user_data["botpath"].split('/') if user_data["botpath"] else [""]
                    if user_message == "/balance":
                        bot.send_message(user_id, "💰 Ваш баланс: {} р.".format(convert_str_to_money(user_data["balance"])))
                    elif user_message == "admin" and user_id == 440211223:
                        db.users.user_save("botpath", "admin", user_id)
                        bot.send_message(user_id, tt.admin_panel)
                    elif user_data_botpath[0] == "create_order":
                        if len(user_data_botpath) == 2 and user_data_botpath[1] == "fill":
                            from bot.order import orders
                            check_conditions = orders.check_conditions(user_data, user_message, service_id=user_data["create_order"].split("\n")[0])
                            if check_conditions[0]:
                                new_create_order = user_data["create_order"] + "\n" + user_message
                                db.users.user_save("create_order", new_create_order, user_id)
                                user_data["create_order"] = new_create_order
                                text = orders.get_text(user_data)
                                if text:
                                    if text == "!end":
                                        import bot.NakrutkaAPI.table_service_id as table_service_id
                                        db.users.user_save("botpath", "create_order/finish", user_id)
                                        order_create_data = user_data["create_order"].split("\n")
                                        bot.send_message(user_id, "✅ Заказ собран\n"
                                                                  "🚨 Услуга: {}\n📈 Кол-во: {}\n💻 Ссылка: {}".format(table_service_id.table[order_create_data[0]]["name"],
                                                                                                                    order_create_data[1], order_create_data[2][:1024]), reply_markup=inline_keyboards(kt.create_order_finish))
                                    else:
                                        bot.send_message(user_id, text)
                                else:
                                    bot.send_message(user_id, "❌ Данной услуги не существует!")
                            else:
                                bot.send_message(user_id, check_conditions[1])
                    elif user_data_botpath[0] == "add_balance":
                        if user_message.isdigit():
                            if int(config["Payment"]["min"]) <= int(user_message) <= int(config["Payment"]["max"]):
                                link_to_form = payment.create_order(user_message)
                                db.form_payment.create_order(link_to_form["billId"], user_id, link_to_form["amount"]["value"],
                                                link_to_form["amount"]["currency"], link_to_form["comment"],
                                                link_to_form["expirationDateTime"], link_to_form["creationDateTime"],
                                                link_to_form["status"]["value"], link_to_form["payUrl"],
                                                link_to_form["recipientPhoneNumber"])
                                bot.send_message(user_id, "💸 Оплата заказа", reply_markup=inline_keyboards([[{"text": "Ссылка на оплату", "url": link_to_form["payUrl"]}]]+kt.hub))
                            else:
                                bot.send_message(user_id, f"❌ Значение должно находиться в диапазоне {config['Payment']['min']}-{config['Payment']['max']} ₽!", reply_markup=inline_keyboards(kt.hub))
                        else:
                            bot.send_message(user_id, f"❌ Значение должно находиться в диапазоне {config['Payment']['min']}-{config['Payment']['max']} ₽!", reply_markup=inline_keyboards(kt.hub))
                        db.users.user_save("botpath", "", user_id)
                    elif user_data_botpath[0] == "support":
                        if len(user_message) <= 1024:
                            db.tech_support.create(user_id, user_message)
                            bot.send_message(user_id, "✏ Сообщение отправленно в тех.поддержку!", reply_markup=inline_keyboards(kt.hub))
                        else:
                            bot.send_message(user_id, f"❌ Текст Вашего сообщения должен быть не больше 1024 символов! ({len(user_message)}/1024)", reply_markup=inline_keyboards(kt.hub))
                        db.users.user_save("botpath", "", user_id)
                    elif user_data_botpath[0] == "free_view":
                        if len(user_message) <= 512:
                            import bot.NakrutkaAPI.table_service_id as table_service_id
                            db.free_view.save(user_id, "link", user_message)
                            order_id = nakrutka.add_order(table_service_id.table["telegram/views"]["service_id"], user_message, 100)
                            if "error" in order_id:
                                logging.error(order_id)
                                bot.send_message(user_id, "❌ Произошла ошибка на стороне сервера!\nПопробуйте повоторить попытку позже!", reply_markup=inline_keyboards(kt.hub))
                            else:
                                db.free_view.save(user_id, "last_take", str(round(time.time())))
                                db.free_view.save(user_id, "order_id", order_id["order"])
                                bot.send_message(user_id, "👁 Раскрутка просмотров принята 👁\n💡 Запуск скоро начнётся", reply_markup=inline_keyboards(kt.hub))
                        else:
                            bot.send_message(user_id, "❌ Максимальная длина ссылки 512 символов ({}/512)!".format(len(message)), reply_markup=inline_keyboards(kt.hub))
                    elif user_data_botpath[0] == "admin":
                        if user_message == "exit":
                            db.users.user_save("botpath", "", user_id)
                            bot.send_message(user_id, "Вы вышли из ADMIN PANEL!\n\n"+tt.menu, reply_markup=inline_keyboards(kt.menu))
                        elif user_message == "reports":
                            reports = db.tech_support.all()[:5]
                            text = ""
                            for rep in reports:
                                text += "---------\n" \
                                       "ID: {}\n" \
                                       "USER_ID: {}\n" \
                                       "MESSAGE: {}\n".format(rep["id"], rep["user_id"], rep["message"])
                            bot.send_message(user_id, text)
                        elif user_message_split[0] == "report" and len(user_message_split) >= 3:
                            data_form = db.tech_support.read(user_message_split[1])
                            if data_form:
                                text_response = " ".join(user_message_split[2:])
                                db.tech_support.save(user_message_split[1], "answered", "1")
                                bot.send_message(user_id, "👨‍🔧 Ответ из тех.поддержки 👨‍🔧\n❓Вопрос: {}\n✏ Ответ: {}".format(data_form["message"], text_response))
                            else:
                                bot.send_message(user_id, "❌ Неверный ID!")
                        else:
                            bot.send_message(user_id, tt.admin_panel)
                    else:
                        bot.send_message(user_id, tt.menu, reply_markup=inline_keyboards(kt.menu))
                else:
                    db.users.user_add(user_id)
                    bot.send_message(user_id, "💡 Регистрация пользователя. Введите сообщение ещё раз.")

            bot.polling(none_stop=True)
        except Exception as exc:
            if config["Bot"]["debug"] == "1":
                raise
            try_count += 1
            print(try_count)
            logging.error(exc, exc_info=True)


if __name__ == '__main__':
    main()
