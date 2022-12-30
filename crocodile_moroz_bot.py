import telebot
from telebot import types
import parse_tost
import random

token = open("security_token.txt", "r", encoding="utf-8").read().rstrip()
crocBot = telebot.TeleBot(token)
videoIdFile = open("./resources/video_id.txt", "r+", encoding="utf-8")
pictureGuessIdFile = open(
    "./resources/picture_id_guess_place.txt", "r+", encoding="utf-8"
)
VIDEO_MESSAGE_ID = videoIdFile.read().rstrip()
PICTURE_MESSAGE_ID = pictureGuessIdFile.read().rstrip()

tosts = []


@crocBot.message_handler(commands=["start", "help"])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Гиви, тост!")
    # item2=types.KeyboardButton("Поздравь")
    markup.add(item1)
    # markup.add(item2)
    crocBot.reply_to(
        message,
        """Привет, уважаемый крокодил. Я знаю много тостов, просто нажми кнопку.""",
        reply_markup=markup,
    )


@crocBot.message_handler(commands=["present", "congratulate", "поздравь"])
def send_congrats(message):
    crocBot.reply_to(message, "Поздравляю с Новым годом!")
    global VIDEO_MESSAGE_ID, videoIdFile, PICTURE_MESSAGE_ID, pictureGuessIdFile
    if VIDEO_MESSAGE_ID == "":
        video = open("./resources/Крокодил мороз бежит поздравлять.mp4", "rb")
        vMsg = crocBot.send_video(message.chat.id, video, supports_streaming=True)
        video.close()
        VIDEO_MESSAGE_ID = vMsg.video.file_id
        videoIdFile.write(VIDEO_MESSAGE_ID)
        videoIdFile.close()
    else:
        crocBot.send_video(message.chat.id, VIDEO_MESSAGE_ID, supports_streaming=True)

    poem = (
        open(
            "./resources/Стих поздравление на Новый год 2023.txt", "r", encoding="utf-8"
        )
        .read()
        .rstrip()
    )
    crocBot.send_message(message.chat.id, poem)
    crocBot.send_message(
        message.chat.id,
        "Угадаем место? Ваши варианты пишите прямо здесь, посмотрим у кого сбылось.",
    )

    if PICTURE_MESSAGE_ID == "":
        pictureGuess = open("./resources/Угадаем место.jpg", "rb")
        picMsg = crocBot.send_photo(message.chat.id, pictureGuess)
        pictureGuess.close()
        PICTURE_MESSAGE_ID = picMsg.photo[0].file_id
        pictureGuessIdFile.write(PICTURE_MESSAGE_ID)
        pictureGuessIdFile.close()
    else:
        crocBot.send_photo(message.chat.id, PICTURE_MESSAGE_ID)


@crocBot.message_handler(commands=["tost", "тост", "гивитост"])
def send_tost(message):
    global tosts
    if len(tosts) == 0:
        tosts = parse_tost.getTosts()
    print("Тостов осталось " + str(len(tosts)))
    randomTostId = random.randint(0, len(tosts) - 1)
    crocBot.reply_to(message, tosts[randomTostId])
    del tosts[randomTostId]


@crocBot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.text == "Гиви, тост!":
        send_tost(message)

    # if message.text == "Поздравь":
    #    send_congrats(message)

    # crocBot.reply_to(message, message.text)


crocBot.infinity_polling()
# crocBot.polling(none_stop=False, interval=1)
