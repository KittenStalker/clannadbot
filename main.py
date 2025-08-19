import telebot, re, random

def contains_word(text, word):
    pattern = r'\b' + re.escape(word) + r'\b'
    return bool(re.search(pattern, text, flags=re.IGNORECASE))

bot = telebot.TeleBot('8055201129:AAHQh8kQZYGRjftT3WL5wPgWmdYhXI8BqE4')

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

exclamation_mark_percent = 0.2
ortho_rika_percent = 0.3
oleg_percent = 0.2

@bot.message_handler(content_types='text')
def message_reply(message):
    #!кланнад и ответ со стикером
    if message.text.lower()=="!кланнад":
        bot.send_sticker(message.chat.id,
                         sticker=nagisa_sad_sticker,
                         reply_to_message_id=message.message_id)

    # не кал
    elif contains_word(message.text, 'не кал'):
        bot.send_sticker(message.chat.id,
                         sticker=denis_reaction_good_sticker)

    # кал
    elif contains_word(message.text, 'кал'):
        bot.send_sticker(message.chat.id,
                         sticker=denis_reaction_bad_sticker)

    # Приветствие для Олега
    elif contains_word(message.text, 'Привет') and contains_word(message.text, 'Олег'):
        bot.send_message(
            message.chat.id,
            text='Привет, Олег!',
        )
        bot.send_sticker(message.chat.id,
                         sticker=nagisa_wow_sticker)

    # Упоминание Олега в чате TODO: сделать с маленьким шансом какую  нибудь реакцию
    elif contains_word(message.text, 'Олег'):
        pass

    # Комнады
    elif message.text.lower()=="!помогите":
        bot.send_message(
            message.chat.id,
            text='Привет! Я Нагиса Лакищтар и я могу отвечать на следующие сообщения: '
                 '\n!кланнад, кал / не кал, Олег'
                 '\nПожалуйста не ',
            reply_to_message_id=message.message_id
        )

    # Ответ Рикой на любое сообщение с восклицательного знака
    elif message.text.startswith('!'):
        if random.random() < exclamation_mark_percent:
            bot.send_message(
                message.chat.id,
                text='Иди нахуй.',
                reply_to_message_id=message.message_id
            )
        if random.random() < ortho_rika_percent:
            random_rika = random.choices(ortho_rika_list, weights=ortho_rika_list_weight, k=1)[0]
            bot.send_sticker(message.chat.id,
                             sticker=random_rika,
                             reply_to_message_id=message.message_id
            )

bot.polling(none_stop=True)

#TODO: обновление статуса онлайн и оффлайн в зависимости от запуска и остановки бота
