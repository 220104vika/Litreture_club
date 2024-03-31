# Подключение библиотеки
import telebot
import time

token = '7133050258:AAFArE5Qf3nJ-WsJIHfMgptXRWifBB648AI'

bot = telebot.TeleBot(token)

user_answers = []
questions = ["Преступления совершены:", "Убийства были:", "Укажите профессию преступника/ов:",
             "В каком году было совершено первое убийство?",
             "К чему отсылает песня Nirvana - Scentless Apprentice на месте обнаружения тела во втором эпизоде?",
             "Что было общим у всех жертв?"]
correct_answers = ["а", "а",
                   ["Учитель литературы","учитель литературы", "Преподаватель литературы", "преподаватель литературы"],
                   "2011",
                   ["к произведению Парфюмер","к книге Парфюмер","парфюмер"],
                   ["Посещали книжный клуб"]]
current_question_index = 0

# Путь к аудиофайлу от Арона
audio_aron = "C:/Users/vichk/Desktop/КК/genius.wav"
audio_genius = "C:/Users/vichk/Desktop/КК/genius.wav"
audio_samantha = "C:/Users/vichk/Desktop/КК/genius.wav"
news = "C:/Users/vichk/Desktop/КК/genius.wav"
night_at_paris =  "C:/Users/vichk/Desktop/КК/genius.wav"
first_material = "C:/Users/vichk/Desktop/КК/genius.wav"
second_material = "C:/Users/vichk/Desktop/КК/genius.wav"
theerd_material = "C:/Users/vichk/Desktop/КК/genius.wav"
fourth_material = "C:/Users/vichk/Desktop/КК/genius.wav"
blank1 = "C:/Users/vichk/Desktop/КК/genius.wav"
blank2 = "C:/Users/vichk/Desktop/КК/genius.wav"

@bot.message_handler(commands=['start'])
def say_hi(message):
    bot.send_message(message.chat.id, 'Здравствуйте. Вы попали в секретный архив Полицейского участка. Напоминанием о правилах пользования!.........Похоже кто-то оставил диктофон с записью.')
    bot.send_audio(message.chat.id, audio=open(audio_aron, 'rb'))
    bot.send_message(message.chat.id, 'Прежде чем ввести код в сейф, отправьте его нам!')


@bot.message_handler(func=lambda message: True)
def get_code(message):
    try:
        number = int(message.text)
        if number == 8616:
            bot.reply_to(message, "Этот код верный! Можете двигаться дальше")
        else:
            bot.reply_to(message, "Неверный код!")
    except ValueError:
        bot.reply_to(message, "Введите код!")


@bot.message_handler(func=lambda message: True)
def send_mess(message):
    bot.send_audio(message.chat.id, audio=open(audio_aron, 'rb'))
    bot.send_message(message.chat.id, 'Бланк....')
    bot.send_audio(message.chat.id, audio=open(audio_aron, 'rb'))


def handle_message(message):
    global current_question_index
    if current_question_index < len(questions):
        user_answers = message.text.lower()
        user_answers.append(message.text)
        current_question_index += 1
        if current_question_index < len(questions):
            bot.send_message(message.chat.id, questions[current_question_index])
        else:
            response = "Ваши ответы:\n" + "\n".join(user_answers) + "\n\nКорректные ответы::\n" + "\n".join(correct_answers)
            bot.send_message(message.chat.id, response)
            user_answers.clear()




















bot.polling()