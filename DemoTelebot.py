# -*- coding utf-8 -*-

import telebot
import config
import os
import flask
from telebot import logger as telebot_logger
import logging
import functions

telebot_logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(config.token)

CHAT_IDS = []
CHAT_ROOM = []

nOfRooms = 0
debuglocal = False

if debuglocal is True:
    API_TOKEN = config.token

    WEBHOOK_HOST = '192.168.90.2/PI2'
    WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
    WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

    WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
    WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

    # Quick'n'dirty SSL certificate generation:
    #
    # openssl genrsa -out webhook_pkey.pem 2048
    # openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
    #
    # When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
    # with the same value in you put in WEBHOOK_HOST
    
    WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
    WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)


    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    #bot = telebot.TeleBot(API_TOKEN)

    app = flask.Flask(__name__)


    # Empty webserver index, return nothing, just http 200
    @app.route('/', methods=['GET', 'HEAD'])
    def index():
        bot.send_message(264405084, "начало обрабатываться")
        return ''
    
    
    # Process webhook calls
    @app.route(WEBHOOK_URL_PATH, methods=['POST'])
    def webhook():
        if flask.request.headers.get('content-type') == 'application/json':
            json_string = flask.request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            flask.abort(403)
    


# '/start' and '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, "Это демонстрационный бот, который ищет для Вас случайного собеседника для общения. Чтоб найти собеседника выполните команду /action")


@bot.message_handler(commands=['action'])
def send_mail_to_another_chat(message):
    global nOfRooms
    if ((not(message.chat.id in CHAT_IDS)) and (not(message.chat.id in CHAT_ROOM))):
        CHAT_IDS.append(message.chat.id)
    alreadyInChat = functions.find_chat_ID_to_send(message.chat.id, nOfRooms, CHAT_ROOM)
    if len(CHAT_IDS) > 1 and alreadyInChat=='notInChat':
        nOfRooms = functions.create_chat_room(int(message.chat.id), nOfRooms, CHAT_IDS, CHAT_IDS)
        bot.send_message(message.chat.id, "Мы нашли вам тайного собеседника, просто напишите ему здесь что-нибудь, и он получит это сообщение от Вас тайно")
    else:
        bot.send_message(message.chat.id, "Мы пока что не нашли вам тайного собеседника. Попробуйте воспользоваться командой поиска еще раз")


@bot.message_handler(commands=["chose_date"])
def ansverCommand(message):
    bot.send_message(message.chat.id, "Пока что ничего не делает")
    #with open('TableTime.csv', newline='') as csvfile:
    #    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    #    for row in spamreader:
    #        if str(row).find('empty') != -1:
    #            bot.send_message(message.chat.id, ', '.join(row))


@bot.message_handler(content_types=["text"])
def repeat_all_messages_to_another_user(message):
    chat_id_to_send = functions.find_chat_ID_to_send(message.chat.id, nOfRooms, CHAT_ROOM)
    if chat_id_to_send == 'notInChat':
        bot.send_message(message.chat.id, "Мы не нашли еще для вас пару, попробуйте еще раз найти собеседника с помощью команды /action")
    else:
        bot.send_message(chat_id_to_send, message.text)


@bot.message_handler(content_types=["sticker", "pinned_message", "photo", "audio"])
def return_to_user(message):
    bot.reply_to(message.chat.id, "Стикер, прикрепленное сообщение, фото или аудио")
    pass


#if debuglocal is True:
#    @server.route("/bot", methods=['POST'])
#    def getMessage():
#        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
#        bot.send_message(264405084, "начало обрабатываться")
#        return "!", 200


#    @server.route("/")
#    def webhook():
#        bot.send_message(264405084, "ставится вебхук")
#        bot.remove_webhook()
#        bot.set_webhook(url="https://demotelegrambot.herokuapp.com")
#        return "!", 200


   
bot.send_message(264405084, "перед запуском сервера")

if debuglocal is True:
     # Remove webhook, it fails sometimes the set if there is a previous webhook
    bot.remove_webhook()
    bot.send_message(264405084, "ставится вебхук")
    # Set webhook
    bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH,
                    certificate=open(WEBHOOK_SSL_CERT, 'r'))

    bot.send_message(264405084, "сервер запущен")
    # Start flask server
    app.run(host=WEBHOOK_LISTEN,
            port=WEBHOOK_PORT,
            ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
            debug=True)
    
   
else:
    bot.send_message(264405084, "лонг поллинг работает")
    #если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
    #Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    bot.polling(none_stop=True)
