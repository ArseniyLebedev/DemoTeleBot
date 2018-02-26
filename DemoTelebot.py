# -*- coding utf-8 -*-
import telebot
from telebot import logger as telebot_logger
import logging
import flask
import config
import User
import sys

sys.stderr = open('error.log', 'w')

telebot_logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(config.token)

#Создать словарь юзеров и заполнять его когда добавляется новый юзер
user_dict = dict()

# Список пользователей находящихся в поиске друга
list_of_friends = list()

# Считывание базы ID из файлов
CHAT_IDS = []
try:
    with open(config.BASE_FILE_NAME, 'r') as file_chat_ids:
        for line in file_chat_ids:
            user_dict[int(line)] = User.ChatUser(int(line)) # создаем юзеров с таким chat ID
            CHAT_IDS.append(int(line))
except FileNotFoundError:
    with open(config.BASE_FILE_NAME, 'w')as file_chat_ids:
        pass

CHAT_ROOM = []

run_on_server = False

if run_on_server is True:
    API_TOKEN = config.token

    WEBHOOK_HOST = '192.168.90.2'
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
    WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN) #чекнуть нужен ли bot или нет


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
            bot.send_message(264405084, "Вебхуки готовы")
            return ''
        else:
            flask.abort(403)
    

# '/start' and '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id,
                     "Это бот, который ищет для Вас случайного собеседника для общения. "
                     "Чтобы найти собеседника выполните команду \n/find_chat_friend")
    # Добавим id диалога с новоприбывшим пользователем бота
    if message.chat.id not in user_dict.keys():
        user_dict[message.chat.id] = User.ChatUser(message.chat.id)
    with open(config.BASE_FILE_NAME, 'r') as file_chat_ids:
        for line in file_chat_ids:
            if int(line) == message.chat.id:
                return
    with open(config.BASE_FILE_NAME, 'a') as file_chat_ids:
        file_chat_ids.writelines(str(message.chat.id) + '\n')


# поиск случайного собеседника
@bot.message_handler(commands=['find_chat_friend'])
def send_mail_to_another_chat(message):
    if message.chat.id not in user_dict.keys():
        user_dict[message.chat.id] = User.ChatUser(message.chat.id)
    # assert isinstance((user_dict[message.chat.id]).in_chat, User.ChatUser)
    if not user_dict[message.chat.id].in_chat:
        list_of_friends.append(user_dict[message.chat.id])
        user_dict[message.chat.id].find_friend(list_of_friends, bot)
    else:
        bot.send_message(message.chat.id,
                         "Мы уже нашли вам тайного собеседника. Просто общайтесь, или сбросьте егоо командой \n/abort_chat_friend")



# сброс диалога со случайным собеседником
@bot.message_handler(commands=["abort_chat_friend"])
def answer_command(message):
    if user_dict[message.chat.id].in_chat:
        user_dict[message.chat.id].abort_chat(bot, None)
    else:
        bot.send_message(message.chat.id,
                         "Вы не участвуете ни в каком диалоге, в начале начните диалог с кем-нибудь при помощи команды \n/find_chat_friend")


# Переслать стикер
@bot.message_handler(content_types=["sticker"])
def return_to_user(message):
    if user_dict[message.chat.id].in_chat:
        bot.send_sticker(user_dict[message.chat.id].id_to_send, message.sticker.file_id)
    else:
        bot.send_message(message.chat.id,
                         "Мы не нашли еще для вас пару, попробуйте еще раз найти собеседника с помощью команды \n/find_chat_friend")


# @bot.message_handler(content_types=["audio"])
# def return_to_user(message):
#     bot.send_audio(message.chat.id, message.audio.file_id)

@bot.message_handler(content_types=["photo"])
def return_to_user(message):
    if user_dict[message.chat.id].in_chat:
        bot.send_photo(user_dict[message.chat.id].id_to_send, message.photo[1].file_id)
    else:
        bot.send_message(message.chat.id,
                         "Мы не нашли еще для вас пару, попробуйте еще раз найти собеседника с помощью команды \n/find_chat_friend")


@bot.message_handler(content_types=["pinned_message", "photo", "audio"])
def return_to_user(message):
    bot.send_message(message.chat.id, "прикрепленное сообщение, фото или аудио")
    #bot.send_audio(message.chat.id, message.audio.file_id)
    pass

@bot.message_handler(content_types=["text"])
def repeat_all_messages_to_another_user(message):
    if user_dict[message.chat.id].in_chat:
        bot.send_message(user_dict[message.chat.id].id_to_send,  message.text)
    else:
        bot.send_message(message.chat.id,
                         "Мы не нашли еще для вас пару, попробуйте еще раз найти собеседника с помощью команды \n/find_chat_friend")


if run_on_server is True:
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
    #если run_on_server не True, значит это запуск с машины разработчика.
    #Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    bot.polling(none_stop=True)
