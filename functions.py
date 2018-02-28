from config import BASE_FILE_NAME
from User import ChatUser


def add_user_to_dict(dict_users, chat_id):
    if chat_id not in dict_users.keys():
        dict_users[chat_id] = ChatUser(chat_id)
        # assert isinstance((dict_users[chat_id]).in_chat, User.ChatUser)

    with open(BASE_FILE_NAME, 'r') as file_chat_ids:
        for line in file_chat_ids:
            if int(line) == chat_id:
                return
    with open(BASE_FILE_NAME, 'a') as file_chat_ids:
        file_chat_ids.writelines(str(chat_id) + '\n')


def is_user_in_chat(dict_users, chat_id):
    add_user_to_dict(dict_users, chat_id)
    if dict_users[chat_id].in_chat:
        return True
    else:
        return False
