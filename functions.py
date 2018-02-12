

def create_chat_room(current_chat_message_id, num_of_rooms, chat_room_list, chat_ids_list):
    chat_room_list.append([])
    chat_room_list[num_of_rooms].append(int(current_chat_message_id))
    if current_chat_message_id in chat_ids_list:
        chat_ids_list.remove(current_chat_message_id)
    else:
        assert "Нарушена логика, проблема при создании комнаты чата"
    chat_room_list[num_of_rooms].append(int(chat_ids_list.pop()))
    num_of_rooms = num_of_rooms + 1
    return num_of_rooms


def find_chat_ID_to_send(current_chat_message_id, num_of_rooms, chat_room_list):
    for i in range(num_of_rooms):
        if chat_room_list[i][0] == current_chat_message_id:
            return chat_room_list[i][1]
        elif chat_room_list[i][1] == current_chat_message_id:
            return chat_room_list[i][0]
    return 'notInChat'
