# -*- coding utf-8 -*-

import telebot
import config
import os
import flask
from telebot import logger as telebot_logger
import logging
import functions
import User

telebot_logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(config.token)

#Создать словарь юзеров и заполнять его когда добавляется новый юзер
user_dict = dict()

# Список пользователей находящихся в поиске друга
list_of_friends = list()

# Считывание базы ID из файлов
CHAT_IDS = []
with  open("chatID.txt", 'r') as file_chat_ids
    for line in file_chat_ids:
        user_dict[int(line)] = User.ChatUser(int(line))
        CHAT_IDS.append(int(line))

CHAT_ROOM = []

# nOfRooms = 0
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
                     "Это демонстрационный бот, который ищет для Вас случайного собеседника для общения. "
                     "Чтобы найти собеседника выполните команду /find_chat_friend")
    # Добавим id диалога с новоприбывшим пользователем бота
    if message.chat.id not in user_dict.keys():
        user_dict[message.chat.id] = User.ChatUser(message.chat.id)
    with open("chatID.txt", 'r') as file_chat_ids
        for line in file_chat_ids:
            if int(line) == message.chat.id:
                return
    with open("chatID.txt", 'a') as file_chat_ids
        file_chat_ids.writelines(str(message.chat.id) + '\n')


# поиск случайного собеседника
@bot.message_handler(commands=['find_chat_friend'])
def send_mail_to_another_chat(message):
    # assert isinstance((user_dict[message.chat.id]).in_chat, User.ChatUser)
    if not user_dict[message.chat.id].in_chat:
        list_of_friends.append(user_dict[message.chat.id], bot)
        user_dict[message.chat.id].find_friend(list_of_friends)
    else:
        bot.send_message(message.chat.id,
                         "Мы уже нашли вам тайного собеседника. Просто общайтесь, или сбросьте егоо командой /abort_chat_friend")

    # global nOfRooms
    # # Сохраняем ChatID текущего пользователя в список
    # if (not(message.chat.id in CHAT_IDS)) and (not(message.chat.id in CHAT_ROOM)):
    #     CHAT_IDS.append(message.chat.id)
    #
    # already_in_chat = functions.find_chat_ID_to_send(message.chat.id, nOfRooms, CHAT_ROOM)
    # if len(CHAT_IDS) > 1 and already_in_chat == 'notInChat':
    #     nOfRooms = functions.create_chat_room(int(message.chat.id), nOfRooms, CHAT_ROOM, CHAT_IDS)
    #     bot.send_message(message.chat.id, "Мы нашли вам тайного собеседника, просто напишите ему здесь что-нибудь, и он получит это сообщение от Вас тайно")
    # else:
    #     bot.send_message(message.chat.id, "Мы пока что не нашли вам тайного собеседника. Попробуйте воспользоваться командой поиска еще раз")

# сброс диалога со случайным собеседником
@bot.message_handler(commands=["abort_chat_friend"])
def answer_command(message):
    if user_dict[message.chat.id].in_chat:
        user_dict[message.chat.id].abort_chat(bot, None)
    else:
        bot.send_message(message.chat.id,
                         "Вы не участвуете ни в каком диалоге, в начале начните диалог с кем-нибудь при помощи команды /find_chat_friend")
    # global nOfRooms
    # bot.send_message(message.chat.id, "Сбрасываем диалог с текущим собеседником")
    # for room in CHAT_ROOM:
    #     for chat_id in room:
    #         if chat_id == message.chat.id:
    #             bot.send_message(room[0], "Диалог сброшен. Чтобы найти нового собеседника нажмите /find_chat_friend")
    #             bot.send_message(room[1], "Диалог сброшен. Чтобы найти нового собеседника нажмите /find_chat_friend")
    #             CHAT_ROOM.remove(room)
    #             nOfRooms -= 1
    #             return
    # bot.send_message(message.chat.id, "Вы не участвуете ни в каком диалоге, в начале начните диалог с кем-нибудь при помощи команды /find_chat_friend")

    #with open('TableTime.csv', newline='') as csvfile:
    #    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    #    for row in spamreader:
    #        if str(row).find('empty') != -1:
    #            bot.send_message(message.chat.id, ', '.join(row))

# Переслать стикер
@bot.message_handler(content_types=["sticker"])
def return_to_user(message):
    if user_dict[message.chat.id].in_chat:
        bot.send_sticker(user_dict[message.chat.id].id_to_send, message.sticker.file_id)
    else:
        bot.send_message(message.chat.id,
                         "Мы не нашли еще для вас пару, попробуйте еще раз найти собеседника с помощью команды /find_chat_friend")


# @bot.message_handler(content_types=["audio"])
# def return_to_user(message):
#     bot.send_audio(message.chat.id, message.audio.file_id)

@bot.message_handler(content_types=["photo"])
def return_to_user(message):
    if user_dict[message.chat.id].in_chat:
        bot.send_photo(user_dict[message.chat.id].id_to_send, message.photo[1].file_id)
    else:
        bot.send_message(message.chat.id,
                         "Мы не нашли еще для вас пару, попробуйте еще раз найти собеседника с помощью команды /find_chat_friend")


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
                         "Мы не нашли еще для вас пару, попробуйте еще раз найти собеседника с помощью команды /find_chat_friend")
    

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
    #если переменной окружения run_on_server не True, значит это запуск с машины разработчика.
    #Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    bot.polling(none_stop=True)
