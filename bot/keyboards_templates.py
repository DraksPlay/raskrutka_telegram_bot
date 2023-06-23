back = [
    [{"text": "◀ Назад", "callback": "back"}]
]

hub = [
    [{"text": "🎩 Меню", "callback": "hub"}]
]

menu = [
    [{"text": "❤‍🔥 Раскрутить ❤‍🔥", "callback": "promote"}],
    [{"text": "👁🤩 БЕСПЛАТНЫЕ ПРОСМОТРЫ 👁🤩", "callback": "free_view"}],
    [{"text": "👥💎 БЕСПЛАТНЫЕ ПОДПИСЧИКИ 👥💎", "callback": "free_followers"}],
    [{"text": "🔍 Инструкия 🔍", "callback": "tutorial"}],
    [{"text": "🎒 Личный кабинет", "callback": "personal_account"}, {"text": "📔 Мои заказы", "callback": "orders"}],
    [{"text": "💰 Баланс", "callback": "balance"}, {"text": "💸 Пополнить баланс", "callback": "add_balance"}],
    [{"text": "👨‍🔧 Тех.поддержка", "callback": "support"}]
]



up_and_down = [
    [{"text": "◀ Назад", "callback": "down"}, {"text": "▶ Вперёд", "callback": "up"}]
]

promote = [
    [{"text": "🇹 Telegram", "callback": "promote/telegram"}],
    [{"text": "🅸 Instagram", "callback": "promote/instagram"}],
    [{"text": "🅑 VK", "callback": "promote/vk"}]
]

promote_telegram = [
    [{"text": "👁 Просмотры", "callback": "promote/telegram/views"}],
    [{"text": "👁 Просмотры на 5 постов", "callback": "promote/telegram/views_5"}],
    [{"text": "👁 Просмотры на 10 постов", "callback": "promote/telegram/views_10"}],
    [{"text": "👁 Просмотры на 20 постов", "callback": "promote/telegram/views_20"}],
    [{"text": "👁 Просмотры на 50 постов", "callback": "promote/telegram/views_50"}],
    [{"text": "👁 Просмотры на 100 постов", "callback": "promote/telegram/views_100"}],
    [{"text": "👥 Подписчики Живые Русские", "callback": "promote/telegram/followers"}],
    [{"text": "👥🇷🇺 Подписчики | Русские | Качественные", "callback": "promote/telegram/followers_ru"}]
]

promote_instagram = [
    [{"text": "👥🇷🇺 Подписчики Русские", "callback": "promote/instagram/followers_ru"}],
    [{"text": "👥🇷🇺 Подписчики Русские - Живые", "callback": "promote/instagram/followers_ru_alive"}],
    [{"text": "👥🤖 Подписчики Боты", "callback": "promote/instagram/followers_bots"}],
    [{"text": "👥🇺🇸 Подписчики США", "callback": "promote/instagram/followers_usa"}],
    [{"text": "❤️Лайки", "callback": "promote/instagram/likes"}],
    [{"text": "❤🇷🇺️ Лайки Русские", "callback": "promote/instagram/likes_ru"}],
    [{"text": "❤ Лайки Живые", "callback": "promote/instagram/likes_alive"}],
    [{"text": "👁 Просмотры - Видео - TV - Reels", "callback": "promote/instagram/views"}],
    [{"text": "👁 Просмотры - Видео + Охват и статистика", "callback": "promote/instagram/views_stats"}],
    [{"text": "👁 Просмотры - Видео + Охват и статистика", "callback": "promote/instagram/views_stats_visit"}],
    [{"text": "👁 Просмотры - Прямой эфир", "callback": "promote/instagram/views_stream"}],
]

promote_vk = [
    [{"text": "👥 Подписчики - Офферные", "callback": "promote/vk/followers_offers"}],
    [{"text": "👥 Подписчики - Качественные", "callback": "promote/vk/followers_top"}],
    [{"text": "👥 Подписчики - Живые", "callback": "promote/vk/followers_alive"}],
    [{"text": "👥🇷🇺 Подписчики - Русские", "callback": "promote/vk/followers_ru"}],
    [{"text": "👫 Друзья", "callback": "promote/vk/friends"}],
    [{"text": "👫️ Друзья - Живые", "callback": "promote/vk/friends_alive"}],
    [{"text": "👫🇷🇺 Друзья - Русские", "callback": "promote/vk/friends_ru"}],
    [{"text": "❤ Лайки - Быстрые", "callback": "promote/vk/likes_fast"}],
    [{"text": "❤ Лайки - Группа/Паблик", "callback": "promote/vk/likes_group"}],
    [{"text": "❤ Лайки - Живые", "callback": "promote/vk/likes_alive"}],
    [{"text": "❤🇷🇺 Лайки - Живые - Россия", "callback": "promote/vk/likes_alive_ru"}],
    [{"text": "👁 Просмотры для группы/паблика", "callback": "promote/vk/views_group"}],
    [{"text": "👁 Просмотры для группы/профиля", "callback": "promote/vk/views_profile"}],
    [{"text": "👁 Просмотры - Клипы", "callback": "promote/vk/views_clips"}],
    [{"text": "🔄 Репосты - Быстрые", "callback": "promote/vk/repost_fast"}],
    [{"text": "🔄 Репосты - Живые", "callback": "promote/vk/repost_alive"}],
]

create_order_finish = [
    [{"text": "⚙ Исправить заказ", "callback": "create_order/edit"}],
    [{"text": "✅ Отправить заказ", "callback": "create_order/complete"}]
]

def create_inline(*args, end: list = None, call=None):
    res = []
    for param in args:
        res += param
    if end:
        for param in end:
            if param == "back":
                obj = list(back)
                obj[0][0]["callback"] = "/".join(call.split("/")[:-1])
                res += obj
            elif param == "hub":
                res += hub
    return res


