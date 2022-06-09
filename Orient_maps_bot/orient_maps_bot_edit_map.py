import orient_maps_bot_types as omb_types
import orient_maps_bot_start as omb_start
import orient_maps_bot_postgre as omb_postgre
from datetime import datetime


def edit_event_date(message):  # получаем дату
    # noinspection PyBroadException
    try:
        if message.text == '/start':
            omb_start.start(message)
            return
        elif message.content_type != 'text':
            omb_types.bot.reply_to(message, 'Неправильный формат даты. Давай по новой.')
            omb_types.bot.register_next_step_handler(message, edit_event_date)
            return

        event_date = message.text
        try:
            event_date = datetime.strptime(event_date, '%d.%m.%Y').date()
        except ValueError:
            omb_types.bot.reply_to(message, 'Неправильный формат даты. Давай по новой.')
            omb_types.bot.register_next_step_handler(message, edit_event_date)
            return

        user_id = message.chat.id
        omap_id = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0] - 1][0]
        omb_postgre.edit_event_date(user_id, omap_id, event_date)

        omb_types.bot.reply_to(message, 'Готово. Дата изменена.')

        omb_types.bot.send_message(user_id, 'Возвращаемся в главное меню',
                                   reply_markup=omb_types.welcome_keyboard(user_id == 366436625))
    except Exception:
        omb_types.bot.reply_to(message, omb_types.errors["omb-001"])


def edit_tags(message):  # получаем дату
    # noinspection PyBroadException
    try:
        if message.text == '/start':
            omb_start.start(message)
            return
        elif message.content_type != 'text':
            omb_types.bot.reply_to(message, 'Не похоже на хэштэги. Давай по новой.')
            omb_types.bot.register_next_step_handler(message, edit_tags)
            return

        tags = message.text

        if len(list(filter(lambda x: x != '#', map(lambda x: x[0], tags.split())))) > 0:
            omb_types.bot.reply_to(message, 'Все хэштэги должны начинаться с символа #. Давай по новой.')
            omb_types.bot.register_next_step_handler(message, edit_tags)
            return

        if len(list(filter(lambda x: x == 0, map(lambda x: len(x[1:]), tags.split())))) > 0:
            omb_types.bot.reply_to(message, 'Путые хэштэги запрещены. Давай по новой.')
            omb_types.bot.register_next_step_handler(message, edit_tags)
            return

        if len(tags.split()) != len(set(tags.split())):
            omb_types.bot.reply_to(message, 'Ладно, дубли сам удалю.')
            tags = ' '.join(set(tags.split()))

        user_id = message.chat.id
        omap_id = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0] - 1][0]
        omb_postgre.edit_tags(user_id, omap_id, tags)

        omb_types.bot.reply_to(message, 'Готово. Хэштэги изменены.')

        omb_types.bot.send_message(user_id, 'Возвращаемся в главное меню',
                                   reply_markup=omb_types.welcome_keyboard(user_id == 366436625))
    except Exception:
        omb_types.bot.reply_to(message, omb_types.errors["omb-001"])


def edit_map_file(message):  # получаем дату
    # noinspection PyBroadException
    try:
        if message.text == '/start':
            omb_start.start(message)
            return
        elif message.content_type == 'document':
            telegram_file_type = 'document'
            name = message.document.file_name
            telegram_file_id = message.document.file_id
        elif message.content_type == 'photo':
            telegram_file_type = 'photo'
            name = message.photo[len(message.photo) - 1].file_id
            telegram_file_id = message.photo[len(message.photo) - 1].file_id
        else:
            omb_types.bot.reply_to(message, omb_types.errors["omb-001"] + '\n'
                                   '*Приложи карту.*\n'
                                   'Для выхода в главное меню: /start',
                                   parse_mode='Markdown')
            omb_types.bot.register_next_step_handler(message, edit_map_file)
            return

        user_id = message.chat.id
        omap_id = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0] - 1][0]

        omb_postgre.edit_map_file(user_id, omap_id, name, telegram_file_type, telegram_file_id)

        omb_types.bot.reply_to(message, 'Готово. Карта заменена.')

        omb_types.bot.send_message(user_id, 'Возвращаемся в главное меню',
                                   reply_markup=omb_types.welcome_keyboard(user_id == 366436625))
    except Exception:
        omb_types.bot.reply_to(message, omb_types.errors["omb-001"])


def edit_geoloc(message):  # получаем дату
    # noinspection PyBroadException
    try:
        if message.text == '/start':
            omb_start.start(message)
            return
        elif message.content_type == 'text':
            try:
                location_lat, location_long = tuple(map(float, map(str.strip, message.text.strip().split(","))))
            except Exception:
                omb_types.bot.reply_to(message, omb_types.errors["omb-003"])
                omb_types.bot.register_next_step_handler(message, edit_geoloc)
                return
            # The latitude must be a number between -90 and 90 and the longitude between -180 and 180.
            if not (-90 < location_lat < 90 and -180 < location_long < 180):
                omb_types.bot.reply_to(message, omb_types.errors["omb-003"])
                omb_types.bot.register_next_step_handler(message, edit_geoloc)
        elif message.content_type == 'location':
            location_lat, location_long = message.location.latitude, message.location.longitude
        else:
            omb_types.bot.reply_to(message, omb_types.errors["omb-003"])
            omb_types.bot.register_next_step_handler(message, edit_geoloc)
            return


        user_id = message.chat.id
        omap_id = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0] - 1][0]

        omb_postgre.edit_geoloc(user_id, omap_id, location_lat, location_long)

        omb_types.bot.reply_to(message, 'Готово. Геолокация изменена.')

        omb_types.bot.send_message(user_id, 'Возвращаемся в главное меню',
                                   reply_markup=omb_types.welcome_keyboard(user_id == 366436625))
    except Exception:
        omb_types.bot.reply_to(message, omb_types.errors["omb-001"])


def edit_first_letter(message):  # получаем дату
    # noinspection PyBroadException
    # try:
        if message.text == '/start':
            omb_start.start(message)
            return
        elif message.content_type != 'text':
            omb_types.bot.reply_to(message, 'Надо одну букву. Давай по новой.')
            omb_types.bot.register_next_step_handler(message, edit_first_letter)
            return
        index = message.text.upper()
        if index != '-' and (len(index) > 1 or not index.isalpha()):
            omb_types.bot.reply_to(message, 'Надо одну букву. Давай по новой.')
            omb_types.bot.register_next_step_handler(message, edit_first_letter)
            return

        user_id = message.chat.id
        omap_id = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0] - 1][0]

        cnt = omb_postgre.edit_first_letter(user_id, omap_id, index)

        omb_types.bot.reply_to(message, 'Готово. Индекс изменён.')
        omb_types.bot.send_message(message.from_user.id,
                                   'Карту нужно убрать в файл с буквой "' + index +
                                   '"\n Номер этой карты в файле: ' + str(cnt[0]))

        omb_types.bot.send_message(user_id, 'Возвращаемся в главное меню',
                                   reply_markup=omb_types.welcome_keyboard(user_id == 366436625))
    # except Exception:
    #     omb_types.bot.reply_to(message, omb_types.errors["omb-001"])
