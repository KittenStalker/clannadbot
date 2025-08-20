import telebot, re, random, enum
from bot_token import bot_token

import requests, logging

bot = telebot.TeleBot(bot_token, skip_pending=True)

# Стикеры
nagisa_sad_sticker = 'CAACAgIAAxkBAAERhJ5oo_YJITxUxUIGXb64Vxd7xqoeLAACg4YAAl2PIUmPmpXMowVj8TYE'
nagisa_wow_sticker = 'CAACAgIAAxkBAAERhLBoo_95eiBEE4mr2P6C3G0kbsKh0QACt4YAAjVnIUk7SNjgkB21-zYE'
denis_reaction_good_sticker = 'CAACAgIAAxkBAAERhKRoo_uKiU4YXCa9VTwgqbJiBUowQAACdkQAAq8cIUtHAVz9Vxhq3TYE'
denis_reaction_bad_sticker = 'CAACAgIAAxkBAAERgxRoo3_gmxcmYnewVH5aC3rOL046KgACL0oAAlnSIUsdIM4-jAPMjDYE'

ortho_rika_angry = 'CAACAgIAAxkBAAERhLhopAAB6_2Bvt_i3lyfARGmsqoCw2oAAk1iAAKjWulJzf3d9T2ARqI2BA'
ortho_rika_calm = 'CAACAgIAAxkBAAERhL5opAEAAX1Nt_nT0mwB_cJyEb-qvXsAAjZiAAL_pOlJ0V4whW_Ptwk2BA'
ortho_rika_hand = 'CAACAgIAAxkBAAERhLxopAAB-3YD7WMf6yayRF4BKK0ofTgAArZ7AAK8ukhLzln_DLZfFyA2BA'
ortho_rika_box = 'CAACAgIAAxkBAAERhO1opA2OlXH-1Gr7ftpcRVsOR9Q3nAACp3cAAlebUUsBAAHcVOqAhfA2BA'

ortho_rika_list = [ortho_rika_angry, ortho_rika_calm, ortho_rika_hand, ortho_rika_box]
ortho_rika_list_weight = [0.4, 0.2, 0.2, 0.2]

bot_status_list = ['Сплю💤...', 'Онлайн🍡']
bot_status = 'Неизвестно'

answer_list = ['Да.', 'Д-да...', 'Конечно!', 'Нет.', 'Ни в коем случае!', 'Ни за что.', 'Возможно', 'Мало вероятно', 'Даже не знаю...']

fuck_you_percent: float = 0.2 # шанс отреагировать на восклицательный знак "иди нахуй"
ortho_rika_percent: float = 0.3 # шанс отреагировать на восклицательный знак Рикой
oleg_percent: float = 0.2 # шанс отреагировать на упоминание Олега

class BotStatus(enum.Enum):
    online = 1
    sleep = 0

# Поиск слова в сообщении
def contains_word(text, word):
    pattern = r'\b' + re.escape(word) + r'\b'
    return bool(re.search(pattern, text, flags=re.IGNORECASE))

# Обновление статуса в описании
def set_status(status: str):
    bot.set_my_short_description(
        short_description='Волшебная девочка таракан'
                          f'\nСтатус: {status}'
                          '\n\nНапишите !помогите для команд'
    )
    description = bot.get_my_short_description()
    print(f'Настоящее описание: {description}')

# Получает случайное изображение с Safebooru по тегу clannad
def safebooru_search(tags, limit):
    try:
        url = "https://safebooru.org/index.php"
        params = {
            'page': 'dapi',
            's': 'post',
            'q': 'index',
            'tags': tags,
            'limit': limit,
            'json': 1
        }

        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()

        data = response.json()
        return data if isinstance(data, list) else []

    except Exception as e:
        logging.error(f"Search error: {e}")
        return []


try:
    # Устанавливаем описание при запуске
    bot_status = bot_status_list[BotStatus.online.value]
    set_status(bot_status)
    print("Bot is active...")

    @bot.message_handler(content_types='text')
    def message_reply(message):
        # !кланнад и ответ со стикером
        if (message.text.lower() == "!кланнад" or message.text.lower() == "! кланнад" or
                message.text.lower() == "!кланад" or message.text.lower() == "! кланад"):
            bot.send_sticker(
                message.chat.id,
                sticker=nagisa_sad_sticker,
                reply_to_message_id=message.message_id
            )

        # Приветствие для Нагисы
        elif contains_word(message.text, 'Привет') and (contains_word(message.text, 'Нагиса')
                                                        or contains_word(message.text, 'Фурукава')):
            bot.send_message(
                message.chat.id,
                text=f'Привет, {message.from_user.first_name}!'
                     f'\nНа данный момент я {bot_status}',
                reply_to_message_id=message.message_id
            )

        # Нагиса это кал?
        elif contains_word(message.text, 'Нагиса') and contains_word(message.text, 'кал') and message.text.endswith('?'):
            if random.randint(0,1) == 0:
                bot.send_message(
                    message.chat.id,
                    text='кал',
                    reply_to_message_id=message.message_id
                )
            else:
                bot.send_message(
                    message.chat.id,
                    text='не кал',
                    reply_to_message_id=message.message_id
                )
            random_rika = random.choices(ortho_rika_list, weights=ortho_rika_list_weight, k=1)[0]
            bot.send_sticker(
                message.chat.id,
                sticker=random_rika,
                reply_to_message_id=message.message_id
            )

        # Нагиса кал
        elif contains_word(message.text, 'Нагиса кал'):
            bot.send_message(
                message.chat.id,
                text='Ты ебало то свое закрой, сынок',
                reply_to_message_id=message.message_id
            )
            random_rika = random.choices(ortho_rika_list, weights=ortho_rika_list_weight, k=1)[0]
            bot.send_sticker(
                message.chat.id,
                sticker=random_rika,
                reply_to_message_id=message.message_id
            )

        # Это правда?
        elif contains_word(message.text, 'Нагиса') and (contains_word(message.text, 'правда') or message.text.endswith('?')):
            bot.send_message(
                message.chat.id,
                text=random.choice(answer_list),
                reply_to_message_id=message.message_id
            )

        # Кланнад картинки
        # elif contains_word(message.text, 'Нагиса') and contains_word(message.text, 'порно'):
        #     posts_found = safebooru_search("clannad", 100)
        #     if not posts_found:
        #         bot.send_message(message.chat.id, "❌ Изображения не найдены")
        #         return
        #     post = random.choice(posts_found)
        #     image_url = f"https://safebooru.org/images/{post['directory']}/{post['image']}"
        #     caption = ("🎨 Рандомная картинка по кланнаду!")
        #     bot.send_photo(
        #         message.chat.id, image_url,
        #         caption=caption,
        #         reply_to_message_id=message.message_id)

        # Упоминание Нагисы
        elif contains_word(message.text, 'Нагиса') or contains_word(message.text, 'Таракан'):
            if random.random() < fuck_you_percent:
                bot.send_message(
                    message.chat.id,
                    text='Иди нахуй.',
                    reply_to_message_id=message.message_id
                )
            random_rika = random.choices(ortho_rika_list, weights=ortho_rika_list_weight, k=1)[0]
            bot.send_sticker(message.chat.id,
                             sticker=random_rika,
                             reply_to_message_id=message.message_id
            )

        # Упоминание Олега в чате TODO: сделать с маленьким шансом какую  нибудь реакцию
        elif contains_word(message.text, 'Олег'):
            pass

        # не кал
        elif contains_word(message.text, 'не кал'):
            bot.send_sticker(
                message.chat.id,
                sticker=denis_reaction_good_sticker
            )

        # кал
        elif contains_word(message.text, 'кал'):
            bot.send_sticker(
                message.chat.id,
                sticker=denis_reaction_bad_sticker
            )

        # Команды
        # TODO: доделать описание команд
        elif message.text.lower() == "!помогите":
            bot.send_message(
                message.chat.id,
                text='Привет! Я Нагиса или же Девочка таракан и я:'
                     '\n* Могу отвечать на !кланнад'
                     '\n* Могу погадать на картах Рё, напишите мое имя с "правда" в предложении или с вопросом в конце.'
                     '\n* Могу определить является ли что либо калом, напишите мое имя с "кал" и вопросов в конце',
                reply_to_message_id=message.message_id
            )

        # Ответ Рикой на любое сообщение с восклицательного знака
        elif message.text.startswith('!'):
            if random.random() < fuck_you_percent:
                bot.send_message(
                    message.chat.id,
                    text='Иди нахуй.',
                    reply_to_message_id=message.message_id
                )
            else:
                bot.send_message(
                    message.chat.id,
                    text='Нет такой команды!',
                    reply_to_message_id=message.message_id
                )
            if random.random() < ortho_rika_percent:
                random_rika = random.choices(ortho_rika_list, weights=ortho_rika_list_weight, k=1)[0]
                bot.send_sticker(message.chat.id,
                                 sticker=random_rika,
                                 reply_to_message_id=message.message_id
                )

    bot.infinity_polling()

finally:
    print("\nИзменяем описание перед выходом...")
    bot_status = bot_status_list[BotStatus.sleep.value]
    set_status(bot_status)


#TODO: в ответку на олега сделать отдельный файл, где будут сообщения по типу "привет поиграй в мою любимую игру "нейм""
#TODO: на малого в ответ добавить "пожалуйста верните" или "я все верну"
#TODO: сделать консоль с командами
#TODO: реакция на данго разными репликами