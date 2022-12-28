import telebot

token = open('security_token.txt', 'r', encoding="utf-8").read().rstrip()
crocBot = telebot.TeleBot(token)

@crocBot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	crocBot.reply_to(message, """Привет, уважаемый крокодил. У нас есть команды, которые тебе понравятся. Выбирай.""")

@crocBot.message_handler(commands=['поздравь', 'congratulate'])
def send_congrats(message):
	crocBot.reply_to(message, "Поздравляю с новым годом")

@crocBot.message_handler(commands=['tost', 'тост', 'гивитост'])
def send_congrats(message):
	crocBot.reply_to(message, "Выпьем за всё хорошее!")

@crocBot.message_handler(func=lambda m: True)
def echo_all(message):
	crocBot.reply_to(message, message.text)

crocBot.infinity_polling()
#crocBot.polling(none_stop=False, interval=1)