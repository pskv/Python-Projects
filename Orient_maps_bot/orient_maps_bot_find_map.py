import orient_maps_bot_types as omb_types
import orient_maps_bot_start as omb_start
import orient_maps_bot_postgre as omb_postgre
from telebot import types
from datetime import datetime


def show_all(message):
    user_id = message.chat.id
    records = omb_postgre.get_all_maps(user_id)

    if len(records) == 0:
        omb_types.bot.send_message(message.chat.id, 'Нет ни одной карты.')
        return

    omb_types.map_pointer[user_id] = [len(records),  # Сколько всего карт в выборке
                                      len(records)]  # Указатель на последнюю карту
    omb_types.user_maps[user_id] = records

    switch_map_init(user_id)


def find_by_first_letter(message):
    # noinspection PyBroadException
    try:
        if message.text == '/start':
            omb_start.start(message)
            return
        elif message.content_type != 'text':
            omb_types.bot.reply_to(message, 'Надо одну букву. Давай по новой.')
            omb_types.bot.register_next_step_handler(message, find_by_first_letter)
            return
        index = message.text.upper()
        if index != '-' and (len(index) > 1 or not index.isalpha()):
            omb_types.bot.reply_to(message, 'Надо одну букву. Давай по новой.')
            omb_types.bot.register_next_step_handler(message, find_by_first_letter)
            return

        user_id = message.chat.id
        records = omb_postgre.get_maps_by_first_letter(user_id, index)

        if len(records) == 0:
            omb_types.bot.send_message(message.chat.id, 'Нет ни одной карты.')
            return

        omb_types.map_pointer[user_id] = [1,  # Указатель на первую карту
                                          len(records)]  # Сколько всего карт в выборке
        omb_types.user_maps[user_id] = records

        switch_map_init(user_id)
    except Exception:
        omb_types.bot.reply_to(message, omb_types.errors["omb-001"])


def find_by_tags(message):
    # noinspection PyBroadException
    try:
        if message.text == '/start':
            omb_start.start(message)
            return
        elif message.content_type != 'text':
            omb_types.bot.reply_to(message, 'Не похоже на хэштэги. Давай по новой.')
            omb_types.bot.register_next_step_handler(message, find_by_tags)
            return

        tag = message.text.lower()

        if tag[0] != '#':
            omb_types.bot.reply_to(message, 'Хэштэг должнен начинаться с символа #. Давай по новой.')
            omb_types.bot.register_next_step_handler(message, find_by_tags)
            return

        if len(tag.split()) > 1:
            omb_types.bot.reply_to(message, 'Нужен один хэштэг. Давай по новой.')
            omb_types.bot.register_next_step_handler(message, find_by_tags)
            return

        if len(tag) == 1:
            omb_types.bot.reply_to(message, 'Пустые хэштэги запрещены. Давай по новой.')
            omb_types.bot.register_next_step_handler(message, find_by_tags)
            return

        user_id = message.chat.id
        records = omb_postgre.get_maps_by_tags(user_id, tag)

        if len(records) == 0:
            omb_types.bot.send_message(message.chat.id, 'Нет ни одной карты.')
            return

        omb_types.map_pointer[user_id] = [1,  # Указатель на первую карту
                                          len(records)]  # Сколько всего карт в выборке
        omb_types.user_maps[user_id] = records

        switch_map_init(user_id)
    except Exception:
        omb_types.bot.reply_to(message, omb_types.errors["omb-001"])


def find_by_geoloc(message):
    # noinspection PyBroadException
    try:
        if message.text == '/start':
            omb_start.start(message)
            return
        if message.content_type == 'text':
            try:
                location_lat, location_long = tuple(map(float, map(str.strip, message.text.strip().split(","))))
            except Exception:
                omb_types.bot.reply_to(message, omb_types.errors["omb-003"])
                omb_types.bot.register_next_step_handler(message, find_by_geoloc)
                return
            # The latitude must be a number between -90 and 90 and the longitude between -180 and 180.
            if not (-90 < location_lat < 90 and -180 < location_long < 180):
                omb_types.bot.reply_to(message, omb_types.errors["omb-003"])
                omb_types.bot.register_next_step_handler(message, find_by_geoloc)
        elif message.content_type == 'location':
            location_lat, location_long = message.location.latitude, message.location.longitude
        else:
            omb_types.bot.reply_to(message, omb_types.errors["omb-003"])
            omb_types.bot.register_next_step_handler(message, find_by_geoloc)
            return

        user_id = message.chat.id
        records = omb_postgre.get_maps_by_geoloc(user_id, location_long, location_lat)

        omb_types.map_pointer[user_id] = [1,  # Указатель на первую карту
                                          len(records),  # Сколько всего карт в выборке
                                          'geoloc']  # режим поиска по геолокации
        omb_types.user_maps[user_id] = records

        omb_types.bot.send_message(user_id, 'Карты отсортированы в порядке удаления от указанной точки:')

        switch_map_init(user_id)
    except Exception:
        omb_types.bot.reply_to(message, omb_types.errors["omb-001"])


def find_by_date(message):
    # noinspection PyBroadException
    try:
        if message.text == '/start':
            omb_start.start(message)
            return
        if message.content_type == 'text':
            try:
                event_date = datetime.strptime(message.text, '%d.%m.%Y').date()
            except ValueError:
                omb_types.bot.reply_to(message, omb_types.errors["omb-004"])
                omb_types.bot.register_next_step_handler(message, find_by_date)
                return
        else:
            omb_types.bot.reply_to(message, omb_types.errors["omb-004"])
            omb_types.bot.register_next_step_handler(message, find_by_date)
            return

        user_id = message.chat.id
        records, pointer = omb_postgre.get_maps_by_date(user_id, event_date)

        omb_types.map_pointer[user_id] = [pointer,  # Указатель на первую карту
                                          len(records)]  # Сколько всего карт в выборке
        omb_types.user_maps[user_id] = records

        omb_types.bot.send_message(user_id,
                                   'Карты отсортированы хронологическом порядке, выбрана ближайшая к указанной дате.')

        switch_map_init(user_id)
    except Exception:
        omb_types.bot.reply_to(message, omb_types.errors["omb-001"])


def switch_map_init(user_id):

    telegram_file_type = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0] - 1][2]
    telegram_file_id = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0] - 1][7]

    if telegram_file_type == 'document':
        msg = omb_types.bot.send_document(user_id, telegram_file_id, caption='-')
        switch_map(msg.chat.id, msg.message_id)
    elif telegram_file_type == 'photo':
        msg = omb_types.bot.send_photo(user_id, telegram_file_id, caption='-')
        switch_map(msg.chat.id, msg.message_id)


def switch_map(user_id, message_id, show_addfiles=False):

    omap = omb_types.Omap(omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0]-1][1])  # Создаём экземпляр класса
    omap.omap_id = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0]-1][0]
    omap.telegram_file_type = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0]-1][2]
    location_long = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0]-1][3]
    location_lat = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0]-1][4]
    omap.location = {'longitude': location_long, 'latitude': location_lat}
    omap.event_date = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0]-1][5]
    omap.tags = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0]-1][6]
    omap.telegram_file_id = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0]-1][7]
    omap.index = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0]-1][8]
    omb_types.omap_dict[user_id] = omap
    index_seq = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0]-1][9]
    addfile_cnt = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0]-1][10]

    if omap.telegram_file_type == 'photo':
        omb_types.bot.edit_message_media(types.InputMediaPhoto(omap.telegram_file_id), user_id, message_id)
    elif omap.telegram_file_type == 'document':
        omb_types.bot.edit_message_media(types.InputMediaDocument(omap.telegram_file_id), user_id, message_id)

    if omap.index == '-':
        map_loc_msg = 'Печатная версия карты отсутствует.'
    else:
        map_loc_msg = 'Карта лежит в файле с буквой "' + str(omap.index) + \
                      '" под номером ' + str(index_seq) + '.'
    if len(omb_types.map_pointer[user_id]) >= 3 and omb_types.map_pointer[user_id][2] == 'geoloc':
        dist_from_point = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0]-1][11]
        map_loc_msg += '\nУдаление от точки поиска: ' + str(dist_from_point) + ' км.'
    omb_types.bot.edit_message_caption('Дата: ' + omap.event_date.strftime('%d.%m.%Y') + '\n' +
                                       omap.tags + '\n' +
                                       map_loc_msg,
                                       user_id, message_id)
    omb_types.bot.edit_message_reply_markup(user_id, message_id,
                                            reply_markup=omb_types.map_switch_keyboard(omb_types.map_pointer[user_id],
                                                                                       addfile_cnt,
                                                                                       show_addfiles, omap.omap_id))


def show_addfile(user_id, message_id, file_id):
    omap = omb_types.Omap(omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0]-1][1])  # Создаём экземпляр класса
    omap.omap_id = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0]-1][0]

    for file in omb_types.map_addfiles[omap.omap_id]:
        if file[0] == file_id:
            telegram_file_type = file[4]
            telegram_file_id = file[3]
            file_type = file[2]
            break

    if telegram_file_type == 'photo':
        omb_types.bot.edit_message_media(types.InputMediaPhoto(telegram_file_id), user_id, message_id)
    elif telegram_file_type == 'document':
        omb_types.bot.edit_message_media(types.InputMediaDocument(telegram_file_id), user_id, message_id)

    omb_types.bot.edit_message_caption(file_type, user_id, message_id)
    omb_types.bot.edit_message_reply_markup(user_id, message_id, reply_markup=omb_types.return_to_map_switch())


def show_geoloc(user_id, message_id):
    omap = omb_types.Omap(omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0]-1][1])  # Создаём экземпляр класса
    omap.omap_id = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0]-1][0]
    location_long = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0]-1][3]
    location_lat = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0]-1][4]
    omap.location = {'longitude': location_long, 'latitude': location_lat}

    omb_types.bot.delete_message(user_id, message_id)
    omb_types.bot.send_location(user_id, omap.location['latitude'], omap.location['longitude'])

    omb_types.bot.send_message(user_id, 'Координаты: ' + str(omap.location['latitude']) + ', '
                               + str(omap.location['longitude']),
                               reply_markup=omb_types.return_to_map_switch_from_geoloc())
