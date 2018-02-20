class ChatUser:
    # in_chat
    list_of_chat_id = []

    def __init__(self, chat_id=None, in_chat=False, male=None):
        self.id_to_send = None
        self.in_chat = in_chat
        self.chat_id = chat_id
        self.male = male
        self.friend = ChatUser  # ссылка на друга User с которым говоришь - не на инстанс класса

    def connect_friend(self, friend):
        """
        :param friend: ChatUser
        :return:
        """
        self.in_chat = True
        self.friend = friend
        self.id_to_send = friend.chat_id
        self.list_of_chat_id.append(friend)
        return 'connected'

    def find_friend(self, list_of_friends_who_want_you: list, bot): #, num_of_rooms, chat_room_list):
        if not self.in_chat:
            for f in list_of_friends_who_want_you:
                # Если мы не в чате, если текущий элемент не мы сами и если мы не подключались к этому пользователю
                if not f.in_chat and f != self: #and f not in self.list_of_chat_id:
                    # указываем данные о подключении
                    f.connect_friend(self)
                    self.connect_friend(f)
                    list_of_friends_who_want_you.remove(f)
                    list_of_friends_who_want_you.remove(self)
                    bot.send_message(f.chat_id, "Мы нашли вам тайного собеседника, "
                                                "просто напишите ему здесь что-нибудь, и он получит это сообщение от Вас тайно")

                    bot.send_message(self.chat_id, "Мы нашли вам тайного собеседника, "
                                                "просто напишите ему здесь что-нибудь, и он получит это сообщение от Вас тайно")
                    return

            bot.send_message(self.chat_id, "Мы пока что не нашли вам тайного собеседника. Попробуйте воспользоваться командой поиска еще раз")
        else:
            raise IOError

    def abort_chat(self, bot, chat_room_list):
        """
        function of aborting two friends
        :param bot: telebot.TeleBot
        :param chat_room_list:
        :return:
        """
        bot.send_message(self.chat_id, "Сбрасываем диалог с текущим собеседником")
        # у того, кого мы заабортили теперь нет друга
        self.friend.__chat_aborted_by_friend(bot, chat_room_list)

        # говорим что мы больше не в чате и у нас нет id чата для отправки и удаляем нашего друга
        self.__abort(chat_room_list)
        bot.send_message(self.chat_id, "Диалог сброшен. Чтобы найти нового собеседника нажмите /find_chat_friend")

    def __abort(self, chat_room_list):
        """
        abort cur instance of class
        :param chat_room_list:
        """
        self.id_to_send = None
        self.in_chat = False
        self.friend = None
        # try:
        #     list(chat_room_list).remove(self)
        # except ValueError:
        #     return

    def __chat_aborted_by_friend(self, bot, chat_room_list=None):
        self.__abort(chat_room_list)
        bot.send_message(self.chat_id, "Диалог с Вами был сброшен собеседником. Не расстраивайтесь, "
                                       "Вы найдете кого-нибудь получше. Чтобы найти нового собеседника нажмите /find_chat_friend")