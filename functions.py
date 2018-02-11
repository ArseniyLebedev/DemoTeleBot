def create_chat_room(current_chat_message_id, num_of_rooms, CHAT_ROOM,CHAT_IDS):
    CHAT_ROOM.append([])
    CHAT_ROOM[num_of_rooms].append(current_chat_message_id)
    if current_chat_message_id in CHAT_IDS:
        CHAT_IDS.remove(current_chat_message_id)
    else:
        assert "Нарушена логика, проблема при создании комнаты чата"
    CHAT_ROOM[num_of_rooms].append(int(CHAT_IDS.pop()))
    num_of_rooms = num_of_rooms + 1
    return num_of_rooms


def find_chat_ID_to_send(current_chat_message_id, num_of_rooms, CHAT_ROOM):
    for i in range(num_of_rooms):
        if CHAT_ROOM[i][0] == current_chat_message_id:
            return CHAT_ROOM[i][1]
        elif CHAT_ROOM[i][1] == current_chat_message_id:
            return CHAT_ROOM[i][0]
    return 'notInChat'
