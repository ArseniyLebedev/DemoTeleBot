# -*- coding utf-8 -*-

import telebot
import config
import os
from flask import Flask, request
from telebot import logger as telebot_logger
import logging

telebot_logger.setLevel(logging.DEBUG)

bot = telebot.TeleBot(config.token)

#telebot_logger.setLevel(DEBUG)
# if "HEROKU" in list(os.environ.keys()):
#     server = Flask(__name__)


server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


@server.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    bot.send_message(264405084, "начало обрабатываться")
    return "!", 200


# @server.route("/bot", methods=['POST'])
# def getMessage():
#     bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
#     bot.send_message(264405084, "начало обрабатываться в другом месте")
#     return "!", 200

@server.route("/")
def webhook():
    bot.send_message(264405084, "ставится вебхук")
    bot.remove_webhook()
    bot.set_webhook(url="https://demotelegrambot.herokuapp.com")
    return "!", 200

print(telebot_logger)

bot.send_message(264405084, "перед запуском сервера")

server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
server = Flask(__name__)

# CHAT_IDS = []
# CHAT_ROOM = []
#
# nOfRooms = 0
#
#
#
# def create_chat_room(currentChatMessageID, numOfRooms):
#     CHAT_ROOM.append([])
#     CHAT_ROOM[nOfRooms].append(int(currentChatMessageID))
#     if currentChatMessageID in CHAT_IDS:
#         CHAT_IDS.remove(currentChatMessageID)
#     else:
#         assert  "Нарушена логика, проблема при создании комнаты чата"
#     CHAT_ROOM[nOfRooms].append(int(CHAT_IDS.pop()))
#     numOfRooms = numOfRooms + 1
#     return numOfRooms
#
# def find_chat_ID_to_send(currentChatMessageID):
#     for i in range(nOfRooms):
#         if CHAT_ROOM[i][0] == currentChatMessageID:
#             return CHAT_ROOM[i][1]
#         elif CHAT_ROOM[i][1] == currentChatMessageID:
#             return CHAT_ROOM[i][0]
#     return 'notInChat'
#
# # Обработчик команд '/start' и '/help'.
# @bot.message_handler(commands=['start', 'help'])
# def handle_start_help(message):
#     bot.send_message(message.chat.id, "Это демонстрационный бот, который ищет для Вас случайного собеседника для общения. Чтоб найти собеседника выполните команду /action")
#
#
# @bot.message_handler(commands=['action'])
# def send_mail_to_another_chat(message):
#     global nOfRooms
#     if ((not(message.chat.id in CHAT_IDS)) and (not(message.chat.id in CHAT_ROOM))):
#         CHAT_IDS.append(message.chat.id)
#     alreadyInChat = find_chat_ID_to_send(message.chat.id)
#     if len(CHAT_IDS) > 1 and alreadyInChat=='notInChat':
#         nOfRooms = create_chat_room(int(message.chat.id), nOfRooms)
#         bot.send_message(message.chat.id, "Мы нашли вам тайного собеседника, просто напишите ему здесь что-нибудь, и он получит это сообщение от Вас тайно")
#     else:
#         bot.send_message(message.chat.id, "Мы пока что не нашли вам тайного собеседника. Попробуйте воспользоваться командой поиска еще раз")
#
#
# @bot.message_handler(commands=["chose_date"])
# def ansverCommand(message):
#     bot.send_message(message.chat.id, "Пока что ничего не делает")
#     #with open('TableTime.csv', newline='') as csvfile:
#     #    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#     #    for row in spamreader:
#     #        if str(row).find('empty') != -1:
#     #            bot.send_message(message.chat.id, ', '.join(row))
#
#
# @bot.message_handler(content_types=["text"])
# def repeat_all_messages_to_another_user(message):
#     chatIDToSend = find_chat_ID_to_send(message.chat.id)
#     if chatIDToSend == 'notInChat':
#         bot.send_message(message.chat.id, "Мы не нашли еще для вас пару, попробуйте еще раз найти собеседника с помощью команды /action")
#     else:
#         bot.send_message(chatIDToSend, message.text)
#
#
# @bot.message_handler(content_types=["sticker", "pinned_message", "photo", "audio"])
# def return_to_user(message):
#     bot.reply_to(message.chat.id, "Стикер, прикрепленное сообщение, фото или аудио")
#     pass


if __name__ == '__main__':
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

#     if "HEROKU" in list(os.environ.keys()):
#         print('heroku')
#     else:
#         # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
#         # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
#         bot.remove_webhook()
#         bot.polling(none_stop=True)
