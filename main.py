# Подключение библиотеки
import telebot
import sqlite3
import time
import enum
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class State(enum.Enum):
    WAITING_CODE = 1
    WAITING_ANS = 2
    WAITING_PASSWORD = 3
    WAITING_LAST_ANS = 4



token = '7133050258:AAFArE5Qf3nJ-WsJIHfMgptXRWifBB648AI'

bot = telebot.TeleBot(token)



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
audio_aron = "resources\арон гот.wav"
audio_genius = "resources\genius.wav"
audio_samantha = "resources\саманта гот..wav"
audio_news = "resources\genius.wav"
# night_at_paris = "resources/genius.wav"
# first_material = "resources/genius.wav"
# second_material = "resources/genius.wav"
# theerd_material = "resources/genius.wav"
# fourth_material = "resources/genius.wav"
# blank1 = "resources/genius.wav"
# blank2 = "resources/genius.wav"
current_state = None

@bot.message_handler(commands=['start'])
def say_hi(message):
    global current_state
    bot.send_message(message.chat.id, 'Здравствуйте. Вы попали в секретный архив Полицейского участка. Напоминанием о правилах пользования!\n \n1. На протяжении расследования мы будем с вами связываться. Ищите подсказки вокруг, внимательно расследуйсте преступления, а только потом связывайтесь с нами. \n \n2. На все ответы нам у вас есть только ОДНА возможность ответить. \n \n Похоже кто-то оставил диктофон с записью.')
    bot.send_audio(message.chat.id, audio=open(audio_aron, 'rb'))
    current_state = State.WAITING_CODE
    time.sleep(60)
    bot.send_message(message.chat.id, 'Прежде чем ввести код в сейф, отправьте его нам! \n На нем стоит защита от перебора комбинаций, Саманта не любит, когда лезут в ее дела.')
    logging.info(f"Пользователь {message.chat.id} на этапе WAITING_CODE")


@bot.message_handler(func=lambda message: current_state == State.WAITING_CODE)
def get_code(message):
    global current_state
    try:
        number = int(message.text)
        if number == 8616:
            current_state = State.WAITING_ANS
            logging.info(f"Пользователь {message.chat.id} на этапе WAITING_ANS")
            bot.reply_to(message, "Этот код верный! Продолжайте свое расследование")
            time.sleep(120)
            send_blank(message)
        else:
            bot.reply_to(message, "Неверный код!")

    except ValueError:
        bot.reply_to(message, "Введите код!")


def send_blank(message):
    bot.send_message(message.chat.id, 'Внимательно ознакомьтесь с материалами с мест преступлений. Прикрепляем диалог из первого эпизода. Дополнительно есть его текстовая расшифровка.')
    bot.send_audio(message.chat.id, audio=open(audio_news, 'rb'))
    ask_questions(message)


user_answers = []
questions = ["Был ли преступник один?", "Были ли преступления случайными?", "Укажите профессию преступника/ов:",
             "В каком году было совершено первое убийство?",
             "К чему отсылает песня Nirvana - Scentless Apprentice на месте обнаружения тела во втором эпизоде?",
             "Что было общим у всех жертв?"]
correct_answers = ["Да", "Нет",
                   "Учитель литературы",
                   "2011",
                   "к произведению Парфюмер",
                   "Посещали книжный клуб"]
current_question_index = 0


def ask_questions(message):
    global current_question_index
    # global current_state
    bot.send_message(message.chat.id, "Ответьте на вопросы основываясь на материалах дел. Имейте в виду, что на каждый вопрос есть только одна попытка. После отправки сообщения невозможно изменить ответ или ответить повторно.")
    bot.send_message(message.chat.id, questions[current_question_index])
    # current_state = State.WAITING_ANS


@bot.message_handler(func=lambda message: current_state == State.WAITING_ANS)
def handler_ans(message):
    global current_state
    global current_question_index

    if current_question_index < len(questions):
        user_answers.append(message.text)
        current_question_index += 1

        if current_question_index < len(questions):
            bot.send_message(message.chat.id, questions[current_question_index])

        else:
            logging.info(f"Пользователь {message.chat.id} на этапе Отправили все ответы")
            bot.send_message(message.chat.id, "Обрабатываем данные.")
            time.sleep(5)
            response = "Ваши ответы:\n" + "\n".join(user_answers) + "\n\nОтветы нашего отдела после некоторых правок:\n"

            for i in range(len(correct_answers)):
                response += f"{questions[i]} - {correct_answers[i]}\n\n"

            bot.send_message(message.chat.id, response, parse_mode="Markdown")
            current_state = State.WAITING_PASSWORD
            user_answers.clear()
            time.sleep(240)
            bot.send_message(message.chat.id, "На какую волну настроенно радио?")




@bot.message_handler(func=lambda message: current_state == State.WAITING_PASSWORD)
def get_new_code(message):
    global current_state
    try:
        number2 = float(message.text)
        if number2 == 98.6:
            bot.reply_to(message, "Волна настроена верно! Ожидайте звуковое оповещение. Скоро вам предстоит снова ответить на наши вопросы. Имейте в виду, что на каждый вопрос есть только одна попытка. После отправки сообщения невозможно изменить ответ или ответить повторно.")
            bot.send_message(message.chat.id, questions_2[current_question_index_2])
            current_state = State.WAITING_LAST_ANS
        else:
            bot.reply_to(message, "Неверная волна!")
    except ValueError:
        bot.reply_to(message, "Неверно")


@bot.message_handler(func=lambda message: current_state == State.WAITING_LAST_ANS)
def handler_mess_2(message):
    global current_question_index_2
    global current_state

    if current_question_index_2 < len(questions_2):
        user_answers.append(message.text)
        current_question_index_2 += 1

        if current_question_index_2 < len(questions_2):
            bot.send_message(message.chat.id, questions_2[current_question_index_2])
            
        else:
            bot.send_message(message.chat.id, "Обрабатываем данные.")
            time.sleep(5)
            response = "Ваши ответы:\n" + "\n".join(user_answers) + "\n\nОтветы нашего отдела после некоторых правок:\n"
            for i in range(len(correct_answers_2)):
                response += f"{questions_2[i]} - {correct_answers_2[i]}\n\n"
            bot.send_message(message.chat.id, response, parse_mode="Markdown")
            user_answers.clear()

    bot.send_audio(message.chat.id, audio=open(audio_samantha, 'rb'))

bot.infinity_polling()