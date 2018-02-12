# -*- coding utf-8 -*-

import telebot
from telebot import TeleBot
import config
import os
from flask import Flask, request
from telebot import logger as telebot_logger
import logging
import functions

telebot_logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(config.token)


CHAT_IDS = []
try:
    file_chat_ids = open("chatID.txt", "r")
    for line in file_chat_ids:
        CHAT_IDS.append(line)
    file_chat_ids.close()
    file_chat_ids.open("chatID.txt", "a")
except:
    file_chat_ids = open("chatID.txt", "w")
    file_chat_ids.close()

CHAT_ROOM = []
nOfRooms = 0
debuglocal = False

if ("HEROKU" in list(os.environ.keys())) or (debuglocal is True):
    server = Flask(__name__)

# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

#
# @bot.message_handler(func=lambda message: True, content_types=['text'])
# def echo_message(message):
#     bot.reply_to(message, message.text)


# '/start' and '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, "Это демонстрационный бот, который ищет для Вас случайного собеседника для общения. Чтоб найти собеседника выполните команду /action")


@bot.message_handler(commands=['action'])
def send_mail_to_another_chat(message):
    global nOfRooms

    if (not(message.chat.id in CHAT_IDS)) and (not(message.chat.id in CHAT_ROOM)):
        CHAT_IDS.append(message.chat.id)
        try:
            file_chat_ids.open("chatID.txt", "a")
            file_chat_ids.writelines(message.chat.id)
            file_chat_ids.close()
        except:
            telebot_logger.error("Can't write chat IDs into the file {}".format(file_chat_ids.name))

    alreadyInChat = functions.find_chat_ID_to_send(message.chat.id, nOfRooms, CHAT_ROOM)
    if len(CHAT_IDS) > 1 and alreadyInChat=='notInChat':
        nOfRooms = functions.create_chat_room(int(message.chat.id), nOfRooms, CHAT_ROOM, CHAT_IDS)
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


@bot.message_handler(content_types=["sticker"])
def return_to_user(message):
    chat_id_to_send = functions.find_chat_ID_to_send(message.chat.id, nOfRooms, CHAT_ROOM)
    if chat_id_to_send == 'notInChat':
        bot.send_message(message.chat.id,
                         "Мы не нашли еще для вас пару, попробуйте еще раз найти собеседника с помощью команды /action")
    else:
        bot.send_sticker(chat_id_to_send, message.sticker.file_id)

@bot.message_handler(content_types=["audio"])
def return_to_user(message):
    bot.send_audio(message.chat.id, message.audio.file_id)

@bot.message_handler(content_types=["photo"])
def return_to_user(message):
    bot.send_photo(message.chat.id, message.photo.file_id)

@bot.message_handler(content_types=["pinned_message", "photo"])
def return_to_user(message):
    bot.send_message(message.chat.id, "прикрепленное сообщение, фото или аудио")
    bot.send_audio(message.chat.id, message.audio.file_id)
    pass

@bot.message_handler(content_types=["text"])
def repeat_all_messages_to_another_user(message):
    chat_id_to_send = functions.find_chat_ID_to_send(message.chat.id, nOfRooms, CHAT_ROOM)
    if chat_id_to_send == 'notInChat':
        bot.send_message(message.chat.id, "Мы не нашли еще для вас пару, попробуйте еще раз найти собеседника с помощью команды /action")
    else:
        bot.send_message(chat_id_to_send, message.text)


if ("HEROKU" in list(os.environ.keys())) or (debuglocal is True):
    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        bot.send_message(264405084, "начало обрабатываться")
        return "!", 200


    @server.route("/")
    def webhook():
        bot.send_message(264405084, "ставится вебхук")
        bot.remove_webhook()
        bot.set_webhook(url="https://demotelegrambot.herokuapp.com")
        return "!", 200

#bot.send_message(264405084, "перед запуском сервера")

if ("HEROKU" in list(os.environ.keys())) or (debuglocal is True):
    bot.send_message(264405084, "сервер запущен")
    PORT = 8443 #int(os.environ.get('PORT', 83))
    server.run(host="0.0.0.0", port=PORT)
    server = Flask(__name__)
else:
    bot.send_message(264405084, "лонг поллинг работает")
    #если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
    #Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    bot.polling(none_stop=True)



#if __name__ == '__main__':
#     if "HEROKU" in list(os.environ.keys()):
#         print('heroku')
#     else:
#         # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
#         # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
#         bot.remove_webhook()
#         bot.polling(none_stop=True)
