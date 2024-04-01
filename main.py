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

user_answers_2 = []
questions_2 = ["Что находилось в посылке, пришедшей на адрес школы для детектива?", ["Что означала поза жертвы в 1м эпизоде? К чему он пытался дать подсказку?"],
               ["На что указывает (как расшифровывается, что означает) записка у жертвы во 2 эпизоде?"],
               ["Записка для Саманты Северли - отсылка к какому произведению?"],
               ["Где может находиться Саманта?"], ["Какие события повлияли на преступника и повлекли за собой совершение преступлений?"]]
correct_answers_2 = ["Голова К. Эттвуда", "Буква А, Подсказка к первой букве в псевдониме убийцы",
                     "5 парта 10й класс. Файф Тэн - псевдоним - Эн Файфт",
                     "Коллекционер", "Взаперти в доме преступника",
                     "Надин мечтала быть писательницей детективов, ее первый же детектив оказался провальным, мечты не осуществились, все рецензии высмеивали и унижали ее труд, ей пришлось вернуться работать в свою собственную школу учителем вместо писательской карьеры"]
current_question_index_2 = 0

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


def send_mess(message):
    bot.send_audio(message.chat.id, audio=open(audio_genius, 'rb'))
    bot.send_message(message.chat.id, 'Бланк....')
    bot.send_audio(message.chat.id, audio=open(news, 'rb'))


def handle_message(message):
    global current_question_index
    if current_question_index < len(questions):
        user_answers.append(message.text)
        current_question_index += 1
        if current_question_index < len(questions):
            bot.send_message(message.chat.id, questions[current_question_index])
        else:
            response = "Ваши ответы:\n" + "\n".join(user_answers) + "\n\nОтветы Саманты::\n"
            for i in range(len(correct_answers)):
                response += f"||{questions[i]}: {correct_answers[i]}||\n"
            # Отправляем сообщение с использованием Markdown
            bot.send_message(message.chat.id, response, parse_mode="Markdown")
            user_answers.clear()


def get_new_code(message):
    bot.send_message(message.chat.id, "Саундтрек из какого фильма Вы только что услышалм?")
    try:
        code = message.text
        if code == "Ночь в Париже" or "ночь в Париже" or "ночь в париже":
            bot.reply_to(message, "Вам стал доступен второй бланк")
            global current_question_index_2
            if current_question_index_2 < len(questions_2):
                user_answers_2.append(message.text)
                current_question_index_2 += 1
                if current_question_index_2 < len(questions_2):
                    bot.send_message(message.chat.id, questions_2[current_question_index_2])
                else:
                    response = "Ваши ответы:\n" + "\n".join(user_answers) + "\n\nОтветы Саманты::\n"
                    for i in range(len(correct_answers_2)):
                        response += f"||{questions_2[i]}: {correct_answers_2[i]}||\n"
                    # Отправляем сообщение с использованием Markdown
                    bot.send_message(message.chat.id, response, parse_mode="Markdown")
                    user_answers.clear()
        else:
            bot.reply_to(message, "Другой саундтрек!")
    except ValueError:
        bot.reply_to(message, "Введите ответ")


def send_2nd(message):
    bot.send_audio(message.chat.id, audio=open(news, 'rb'))


bot.polling()
