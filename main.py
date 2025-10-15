import telebot, re, random
from telebot.types import ReactionTypeEmoji

from bot_token import bot_token

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

answer_list = ['Да.', 'Д-да...', 'Конечно!', 'Нет.', 'Ни в коем случае!', 'Ни за что.', 'Возможно', 'Мало вероятно', 'Даже не знаю...', 'Нужно подумать...']
curse_list = ['Иди нахуй.', 'Ты за кого меня держишь', 'Не хочу.', 'Нипааа~', 'Я тебе не Олег']

user_blacklist = {
    6564147478: 'Малой',
}
admin = '1070873517'

dice_warning = 2
dice_counter = 0

curse_percent: float = 0.2 # шанс отреагировать на восклицательный знак ругательством
ortho_rika_percent: float = 0.3 # шанс отреагировать на восклицательный знак Рикой
oleg_percent: float = 0.2 # шанс отреагировать на упоминание Олега

# Поиск слова в сообщении
def contains_word(text, word):
    pattern = r'\b' + re.escape(word) + r'\b'
    return bool(re.search(pattern, text, flags=re.IGNORECASE))

# Обновление статуса в описании
def set_status(status: str):
    bot.set_my_short_description(
        short_description='Волшебная девочка таракан'
                          '\n\nНапишите !помогите для команд'
    )
    description = bot.get_my_short_description()
    print(f'Настоящее описание: {description}')

# Проверка на блэклист
def is_user_blacklisted(user_id: int) -> bool:
    return user_id in user_blacklist

# Проверка сообщения
def should_process_message(message) -> bool:
    if is_user_blacklisted(message.from_user.id):
        print(f"Сообщение от заблокированного пользователя {user_blacklist[message.from_user.id]} "
              f"({message.from_user.first_name} {message.from_user.last_name}) проигнорировано")
        return False
    return True

# Отправление случайного стикера с Рикой
def send_random_rika(message):
    random_rika = random.choices(ortho_rika_list, weights=ortho_rika_list_weight, k=1)[0]
    bot.send_sticker(
        message.chat.id,
        sticker=random_rika,
        reply_to_message_id=message.message_id
    )

def send_random_curse(message):
    bot.send_message(
        message.chat.id,
        text=random.choice(curse_list),
        reply_to_message_id = message.message_id
    )

def handle_clannad_command(message):
    bot.send_sticker(
        message.chat.id,
        sticker=nagisa_sad_sticker,
        reply_to_message_id=message.message_id
    )

def handle_hello_command(message):
    bot.send_message(
        message.chat.id,
        text=f'Привет, {message.from_user.first_name}!',
        reply_to_message_id=message.message_id
    )

def handle_kal_question_command(message):
    if random.randint(0, 1) == 0:
        bot.send_message(
            message.chat.id,
            text='Кал.',
            reply_to_message_id=message.message_id
        )
    else:
        bot.send_message(
            message.chat.id,
            text='Не кал!',
            reply_to_message_id=message.message_id
        )
    send_random_rika(message)

def handle_truth_command(message):
    bot.send_message(
        message.chat.id,
        text=random.choice(answer_list),
        reply_to_message_id=message.message_id
    )

def handle_exclamation_command(message):
    if random.random() < curse_percent:
        send_random_curse(message)
    else:
        bot.send_message(
            message.chat.id,
            text='Нет такой команды!',
            reply_to_message_id=message.message_id
        )
    if random.random() < ortho_rika_percent:
        send_random_rika(message)

def handle_help_command(message):
    bot.send_message(
        message.chat.id,
        text='Привет! Я Нагиса или же Девочка таракан и я:'
             '\n* Могу отвечать на !кланнад'
             '\n* Могу погадать на картах Рё, напишите мое имя с вопросом в конце.'
             '\n* Могу определить является ли что либо калом, напишите мое имя с "кал" и вопросов в конце'
             '\n* Могу пересказать слова, достаточно написать "Нагиса скажи"',
        reply_to_message_id=message.message_id
    )

def handle_say_command(message):
    if random.random() < curse_percent:
        send_random_curse(message)
    else:
        said_text = message.text.lower().split('скажи ')[1].capitalize()
        bot.send_message(
            message.chat.id,
            text=said_text,
        )

def handle_nagisa_mention(message):
    if random.random() < curse_percent:
        send_random_curse(message)
    else:
        bot.send_message(
            message.chat.id,
            text='Слушаюсь!',
        )
    send_random_rika(message)

#TODO
def handle_oleg_mention(message):
    pass

def handle_kal_mention(message):
    bot.send_sticker(
        message.chat.id,
        sticker=denis_reaction_good_sticker
    )

def handle_not_kal_mention(message):
    bot.send_sticker(
        message.chat.id,
        sticker=denis_reaction_bad_sticker
    )

def handle_info_command(message):
    user_id = message.from_user.id
    print(f"\nИмя: {message.from_user.first_name}"
          f"\nФамилия: {message.from_user.last_name}"
          f"\nЮзернейм: {message.from_user.username}"
          f"\nТелеграмм ID: {user_id}")


print('Нагиса работает...')

# Обработчик сообщений
@bot.message_handler(content_types=['text'])
def message_reply(message):
    if not should_process_message(message):
        return

    if message.from_user.id == admin: # ид Гебуры 539065613
        bot.set_message_reaction(message.chat.id, message.id, [ReactionTypeEmoji('👍')], is_big=False)

    if contains_word(message.text, 'Нагиса') or contains_word(message.text, 'Фурукава'):

        # Нагиса это кал?
        if contains_word(message.text, 'кал') and message.text.endswith('?'):
            handle_kal_question_command(message)

        # Скажи
        elif contains_word(message.text, 'Скажи'):
            handle_say_command(message)

        # Приветствие для Нагисы
        elif contains_word(message.text, 'Привет'):
            handle_hello_command(message)

        # Гадание
        elif message.text.endswith('?'):
            handle_truth_command(message)

        # Простое упоминание Нагисы
        else:
            handle_nagisa_mention(message)

    # Упоминание Олега в чате TODO: сделать с маленьким шансом какую  нибудь реакцию
    elif contains_word(message.text, 'Олег'):
        handle_oleg_mention(message)

    # не кал
    elif contains_word(message.text, 'не кал'):
        handle_kal_mention(message)

    # кал
    elif contains_word(message.text, 'кал'):
        handle_not_kal_mention(message)

    # !кланнад и ответ со стикером
    elif (message.text.lower() == "!кланнад" or message.text.lower() == "! кланнад" or
            message.text.lower() == "!кланад" or message.text.lower() == "! кланад"):
        handle_clannad_command(message)

    # Команды
    # TODO: доделать описание команд
    elif message.text.lower() == "!помогите":
        handle_help_command(message)

    # Ответ Рикой на любое сообщение с восклицательного знака
    elif message.text.startswith('!'):
        handle_exclamation_command(message)

    # handle_info_command(message)

prev_dice_message = 0

# Удаление дайсов
@bot.message_handler(content_types=['dice'])
def handle_text(message):
    if message.dice:
        bot.delete_message(message.chat.id, prev_dice_message)




bot.infinity_polling()



#TODO: в ответку на олега сделать отдельный файл, где будут сообщения по типу "привет поиграй в мою любимую игру "нейм""
#TODO: на малого в ответ добавить "пожалуйста верните" или "я все верну"
#TODO: сделать консоль с командами
#TODO: реакция на данго разными репликами