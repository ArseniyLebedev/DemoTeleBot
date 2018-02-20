class User:
    # in_chat
    list_of_aborted_chat_id = []
    def __init__(self, in_chat=False, chat_id=None, male=None):
        self.id_to_send = None
        self.in_chat = in_chat
        self.chat_id = chat_id
        self.male = male
        self.friend = User # ссылка на друга User с которым говоришь - не на инстанс класса

    def find_friend(self, list_of_friends_who_want_you, num_of_rooms, chat_room_list):
        if self.in_chat:
            return self.id_to_send
        else:
            id
            return None

    def abort(self, chat_room_list):
        self.id_to_send = None
        self.in_chat = False
        self.friend = None
        list(chat_room_list).remove(self)

    def abort_chat(self, bot, chat_room_list):
        bot.send_message(self.chat_id, "Сбрасываем диалог с текущим собеседником")
        bot.send_message(self.chat_id, "Диалог сброшен. Чтобы найти нового собеседника нажмите /find_chat_friend")

        # у того, кого мы заабортили теперь нет друга
        self.friend.chat_aborted_by_friend(bot, chat_room_list)

        # говорим что мы больше не в чате и у нас нет id чата для отправки и удаляем нашего друга
        self.abort(chat_room_list)

    def chat_aborted_by_friend(self, bot, chat_room_list=None):
        self.abort(chat_room_list)
        bot.send_message(self.chat_id, "Диалог с Вами был сброшен собеседником. Не расстраивайтесь, Вы найдете кого-нибудь получше. Чтобы найти нового собеседника нажмите /find_chat_friend")


            def find_chat_ID_to_send(current_chat_message_id, num_of_rooms, chat_room_list):
                for i in range(num_of_rooms):
                    if chat_room_list[i][0] == current_chat_message_id:
                        return chat_room_list[i][1]
                    elif chat_room_list[i][1] == current_chat_message_id:
                        return chat_room_list[i][0]
                return 'notInChat'
