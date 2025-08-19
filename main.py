import telebot, re

def contains_word(text, word):
    pattern = r'\b' + re.escape(word) + r'\b'
    return bool(re.search(pattern, text, flags=re.IGNORECASE))

bot = telebot.TeleBot('8055201129:AAHQh8kQZYGRjftT3WL5wPgWmdYhXI8BqE4')

nagisa_sad_sticker = 'CAACAgIAAxkBAAERhJ5oo_YJITxUxUIGXb64Vxd7xqoeLAACg4YAAl2PIUmPmpXMowVj8TYE'
denis_reaction_sticker = 'CAACAgIAAxkBAAERgxRoo3_gmxcmYnewVH5aC3rOL046KgACL0oAAlnSIUsdIM4-jAPMjDYE'

@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text.lower()=="!кланнад":
        bot.send_sticker(message.chat.id,
                         sticker=nagisa_sad_sticker)

        # with open('media/nagisa.gif', 'rb') as img:
        #     bot.send_animation(
        #         chat_id=message.chat.id,
        #         animation=img,
        #         reply_to_message_id=message.message_id
        #     )

    elif contains_word(message.text, 'кал'):
        bot.send_sticker(message.chat.id,
                         sticker=denis_reaction_sticker)

    elif message.text.lower()=="!помогите":
        bot.send_message(
            message.chat.id,
            text='В настоящий момент работают команды: !кланнад, кал',
            reply_to_message_id=message.message_id
        )

bot.polling(none_stop=True)