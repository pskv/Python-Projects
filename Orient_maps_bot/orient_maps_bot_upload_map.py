from telebot import types
from datetime import date, timedelta, datetime
import orient_maps_bot_types as omb_types
import orient_maps_bot_start as omb_start
import orient_maps_bot_postgre as omb_postgre
import orient_maps_bot_find_map as omb_find_map

addfile_dict = {}


def upload_map(message):  # получаем карту
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
            omb_types.bot.register_next_step_handler(message, upload_map)
            return

        chat_id = message.chat.id
        omap = omb_types.Omap(name)
        omap.telegram_file_type = telegram_file_type
        omap.telegram_file_id = telegram_file_id
        omap.owner = message.from_user.id
        omb_types.omap_dict[chat_id] = omap

        omb_types.bot.reply_to(message, 'Принято.')
        omb_types.bot.send_message(message.from_user.id,
                                   '*Приложи геолокацию*.\n'
                                   'Либо используй команду /back чтобы вернуться к загрузке карт.',
                                   parse_mode='Markdown')
        omb_types.bot.register_next_step_handler(message, get_location)  # следующий шаг – функция Get_location
    except Exception:
        omb_types.bot.reply_to(message, omb_types.errors["omb-001"])


def get_location(message):  # получаем координаты
    # noinspection PyBroadException
    try:
        if message.text == '/start':
            omb_start.start(message)
            return
        if message.text == '/back':
            omb_types.bot.send_message(message.chat.id,
                                       'Хорошо, вернёмся к картам.\n*Приложи карту.*',
                                       parse_mode='Markdown')
            omb_types.bot.register_next_step_handler(message, upload_map)  # следующий шаг – функция upload_map
            return

        if message.content_type == 'text':
            try:
                location_lat, location_long = tuple(map(float, map(str.strip, message.text.strip().split(","))))
            except Exception:
                omb_types.bot.reply_to(message, omb_types.errors["omb-003"])
                omb_types.bot.register_next_step_handler(message, get_location)
                return
            # The latitude must be a number between -90 and 90 and the longitude between -180 and 180.
            if not (-90 < location_lat < 90 and -180 < location_long < 180):
                omb_types.bot.reply_to(message, omb_types.errors["omb-003"])
                omb_types.bot.register_next_step_handler(message, get_location)
        elif message.content_type == 'location':
            location_lat, location_long = message.location.latitude, message.location.longitude
        else:
            omb_types.bot.reply_to(message, omb_types.errors["omb-003"])
            omb_types.bot.register_next_step_handler(message, get_location)
            return

        chat_id = message.chat.id
        omap = omb_types.omap_dict[chat_id]
        omap.location = {'longitude': location_long, 'latitude': location_lat}

        omb_types.bot.reply_to(message, 'Принято.')

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("Сегодня", "Вчера")
        omb_types.bot.send_message(message.from_user.id,
                                   "*Когда был старт?* (укажи дату в формате *DD.MM.YYYY*)\n"
                                   "Либо используй команду /back чтобы вернуться к геолокации.",
                                   parse_mode='Markdown',
                                   reply_markup=markup)

        omb_types.bot.register_next_step_handler(message, get_event_date)  # следующий шаг – функция Get_event_date
    except Exception:
        omb_types.bot.reply_to(message, omb_types.errors["omb-001"])


def get_event_date(message):  # получаем дату
    # noinspection PyBroadException
    try:
        if message.text == '/start':
            omb_start.start(message)
            return
        elif message.text == '/back':
            omb_types.bot.send_message(message.chat.id,
                                       'Хорошо, вернёмся к геолокации. *Приложи геолокацию.*',
                                       parse_mode='Markdown',
                                       reply_markup=types.ReplyKeyboardRemove())
            omb_types.bot.register_next_step_handler(message, get_location)
            return
        elif message.content_type != 'text':
            omb_types.bot.reply_to(message, 'Неправильный формат даты. Давай по новой.')
            omb_types.bot.register_next_step_handler(message, get_event_date)
            return

        event_date = message.text
        if event_date == 'Сегодня':
            event_date = date.today()
        elif event_date == 'Вчера':
            event_date = date.today() - timedelta(days=1)
        else:
            try:
                event_date = datetime.strptime(event_date, '%d.%m.%Y').date()
            except ValueError:
                omb_types.bot.reply_to(message, 'Неправильный формат даты. Давай по новой.')
                omb_types.bot.register_next_step_handler(message, get_event_date)
                return

        chat_id = message.chat.id
        omap = omb_types.omap_dict[chat_id]
        omap.event_date = event_date

        omb_types.bot.reply_to(message, 'Принято.', reply_markup=types.ReplyKeyboardRemove())

        omb_types.bot.send_message(message.from_user.id,
                                   "*Укажи хэштэги*\n"
                                   "Либо используй команду /back чтобы вернуться к дате.",
                                   parse_mode='Markdown')
        omb_types.bot.register_next_step_handler(message, get_tags)  # следующий шаг – функция Get_tags
    except Exception:
        omb_types.bot.reply_to(message, omb_types.errors["omb-001"])


def get_tags(message):  # получаем хэштэги
    # noinspection PyBroadException
    try:
        if message.text == '/start':
            omb_start.start(message)
            return
        elif message.text == '/back':
            omb_types.bot.send_message(message.chat.id,
                                       'Хорошо, вернёмся к дате. Укажи дату в формате *DD.MM.YYYY*',
                                       parse_mode='Markdown')
            omb_types.bot.register_next_step_handler(message, get_event_date)
            return
        elif message.content_type != 'text':
            omb_types.bot.reply_to(message, 'Не похоже на хэштэги. Давай по новой.')
            omb_types.bot.register_next_step_handler(message, get_tags)
            return

        tags = message.text

        if len(list(filter(lambda x: x != '#', map(lambda x: x[0], tags.split())))) > 0:
            omb_types.bot.reply_to(message, 'Все хэштэги должны начинаться с символа #. Давай по новой.')
            omb_types.bot.register_next_step_handler(message, get_tags)
            return

        if len(list(filter(lambda x: x == 0, map(lambda x: len(x[1:]), tags.split())))) > 0:
            omb_types.bot.reply_to(message, 'Путые хэштэги запрещены. Давай по новой.')
            omb_types.bot.register_next_step_handler(message, get_tags)
            return

        if len(tags.split()) != len(set(tags.split())):
            omb_types.bot.reply_to(message, 'Ладно, дубли сам удалю.')
            tags = ' '.join(set(tags.split()))

        chat_id = message.chat.id
        omap = omb_types.omap_dict[chat_id]
        omap.tags = tags

        omb_types.bot.reply_to(message, 'Принято.')

        omb_types.bot.send_message(message.from_user.id,
                                   "Укажи *индекс* названия карты (в какой файл убирать карту)\n"
                                   "Если печатной версии карты нет, то напиши '-'\n"
                                   "Либо используй команду /back чтобы вернуться к хэштэгам.",
                                   parse_mode='Markdown')
        omb_types.bot.register_next_step_handler(message, get_first_letter)  # следующий шаг – функция Get_first_letter
    except Exception:
        omb_types.bot.reply_to(message, omb_types.errors["omb-001"])


def get_first_letter(message):  # получаем первую букву названия карты
    # noinspection PyBroadException
    try:
        if message.text == '/start':
            omb_start.start(message)
            return
        elif message.text == '/back':
            omb_types.bot.send_message(message.chat.id,
                                       'Хорошо, вернёмся к хэштэгам. *Укажи хэштэги*',
                                       parse_mode='Markdown')
            omb_types.bot.register_next_step_handler(message, get_tags)
            return
        elif message.content_type != 'text':
            omb_types.bot.reply_to(message, 'Надо одну букву. Давай по новой.')
            omb_types.bot.register_next_step_handler(message, get_first_letter)
            return

        index = message.text.upper()
        if index != '-' and (len(index) > 1 or not index.isalpha()):
            omb_types.bot.reply_to(message, 'Надо одну букву. Давай по новой.')
            omb_types.bot.register_next_step_handler(message, get_first_letter)
            return

        chat_id = message.chat.id
        omap = omb_types.omap_dict[chat_id]
        omap.index = index

        omb_types.bot.reply_to(message, 'Принято.')

        omb_types.bot.send_message(message.from_user.id, 'Вот что получилось: \n ~~~~~~~~~~~~~~ \n'
                                   + 'Координаты: ' + str(omap.location['latitude']) + ', ' +
                                   str(omap.location['longitude']) + '\n'
                                   + 'Дата: ' + str(omap.event_date) + '\n'
                                   + 'Хэштэги: ' + omap.tags + '\n'
                                   + 'Первая буква названия: ' + omap.index + '\n'
                                   + '~~~~~~~~~~~~~~ \n'
                                   )
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("Да", "Нет")
        omb_types.bot.send_message(message.from_user.id,
                                   "*Сохраняем?*\n"
                                   "Если нужно вернуться к первой букве названия карты, то используй команду /back.",
                                   reply_markup=markup,
                                   parse_mode='Markdown')

        omb_types.bot.register_next_step_handler(message, save_data_to_db)  # следующий шаг – функция Save_data_to_db

    except Exception:
        omb_types.bot.reply_to(message, omb_types.errors["omb-001"])


def save_data_to_db(message):
    # noinspection PyBroadException
    try:
        if message.text == '/start':
            omb_start.start(message)
            return
        elif message.text == '/back':
            omb_types.bot.send_message(message.chat.id,
                                       'Хорошо, вернёмся. Укажи *первую букву* названия карты',
                                       parse_mode='Markdown',
                                       reply_markup=types.ReplyKeyboardRemove())
            omb_types.bot.register_next_step_handler(message, get_first_letter)
            return
        elif message.text == "Да":
            chat_id = message.chat.id
            omap = omb_types.omap_dict[chat_id]
            cnt = omb_postgre.save_map_to_db(omap)
            if omap.index == '-':
                omb_types.bot.send_message(message.from_user.id,
                                           'Готово. Данные загружены в БД.\n',
                                           reply_markup=types.ReplyKeyboardRemove())
            else:
                omb_types.bot.send_message(message.from_user.id,
                                           'Готово. Данные загружены в БД.\n'
                                           'Карту нужно убрать в файл с буквой "' + omap.index +
                                           '"\n Номер этой карты в файле: ' + str(cnt[0]),
                                           reply_markup=types.ReplyKeyboardRemove())
            omb_start.start(message)
            return

        elif message.text == "Нет":
            omb_types.bot.send_message(message.from_user.id, 'Ну ок.', reply_markup=types.ReplyKeyboardRemove())

    except Exception as e:
        omb_postgre.log_db('save_data_to_db', message.from_user.id, str(e))
        omb_types.bot.reply_to(message, omb_types.errors["omb-001"])


def add_file_cmd(message):

    chat_id = message.chat.id
    if chat_id not in omb_types.omap_dict:
        omb_types.bot.send_message(message.chat.id, "Не выбрана карта для добавления файлов")
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Распечатка", "Трэк", "Наложенный трэк")
    omb_types.bot.send_message(message.chat.id, "Что это будет за файл?", reply_markup=markup)
    omb_types.bot.register_next_step_handler(message, add_file_type)  # следующий шаг – функция add_file_type


def add_file_type(message):
    # noinspection PyBroadException
    try:
        if message.content_type == 'text' and message.text == '/start':
            omb_start.start(message)
            return
        elif message.content_type != 'text':
            omb_types.bot.reply_to(message,
                                   'Нужен текст.\n'
                                   'Давай по новой.\n'
                                   'Для выхода в главное меню: /start',
                                   parse_mode='Markdown')
            omb_types.bot.register_next_step_handler(message, add_file)
            return

        chat_id = message.chat.id
        omap = omb_types.omap_dict[chat_id]
        addfile = omb_types.Addfile(omap.omap_id, message.text)
        addfile_dict[chat_id] = addfile

        omb_types. bot.reply_to(message, 'Принято.', reply_markup=types.ReplyKeyboardRemove())

        omb_types.bot.send_message(message.chat.id,
                                   "*Приложи файл.*\n"
                                   "Если нужно вернуться к описанию файла, то используй команду /back.",
                                   parse_mode='Markdown')
        omb_types.bot.register_next_step_handler(message, add_file)  # следующий шаг – функция add_file

    except Exception as e:
        omb_postgre.log_db('add_file_type', message.from_user.id, str(e))
        omb_types.bot.reply_to(message, omb_types.errors["omb-001"])


def add_file(message):
    # noinspection PyBroadException
    try:

        if message.content_type == 'text' and message.text == '/start':
            omb_start.start(message)
            return
        elif message.content_type == 'text' and message.text == '/back':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add("Распечатка", "Трэк", "Наложенный трэк")
            omb_types.bot.send_message(message.chat.id, "Хорошо, вернёмся.\nЧто это будет за файл?",
                                       reply_markup=markup)
            omb_types.bot.register_next_step_handler(message, add_file_type)  # следующий шаг – функция add_file_type
            return
        elif message.content_type == 'document':
            telegram_file_type = 'document'
            telegram_file_id = message.document.file_id
        elif message.content_type == 'photo':
            telegram_file_type = 'photo'
            telegram_file_id = message.photo[len(message.photo) - 1].file_id
        else:
            omb_types.bot.reply_to(message,
                                   'Не похоже на файл.\n'
                                   'Давай по новой. *Приложи файл.*\n'
                                   'Для выхода в главное меню: /start',
                                   parse_mode='Markdown')
            omb_types.bot.register_next_step_handler(message, add_file)
            return

        chat_id = message.chat.id
        additional_file = addfile_dict[chat_id]
        additional_file.telegram_file_id = telegram_file_id
        additional_file.telegram_file_type = telegram_file_type

        omb_types.bot.reply_to(message, 'Принято.', reply_markup=None)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("Да", "Нет")
        omb_types.bot.send_message(message.from_user.id,
                                   "*Сохраняем?*\n"
                                   "Если нужно вернуться к загрузке файла, то используй команду /back.",
                                   reply_markup=markup,
                                   parse_mode='Markdown')

        omb_types.bot.register_next_step_handler(message, save_file_to_db)  # следующий шаг – функция save_file_to_db

    except Exception as e:
        omb_postgre.log_db('add_file', message.from_user.id, str(e))
        omb_types.bot.reply_to(message, omb_types.errors["omb-001"])


def save_file_to_db(message):
    # noinspection PyBroadException
    try:
        if message.content_type == 'text' and message.text == '/start':
            omb_start.start(message)
            return
        elif message.content_type == 'text' and message.text == '/back':
            omb_types.bot.send_message(message.chat.id,
                                       'Хорошо, вернёмся. *Приложи файл.*',
                                       parse_mode='Markdown',
                                       reply_markup=None)
            omb_types.bot.register_next_step_handler(message, add_file)
            return
        elif message.text == "Да":
            chat_id = message.chat.id
            addfile = addfile_dict[chat_id]
            omb_postgre.save_file_to_db(addfile, chat_id)
            omb_types.bot.send_message(message.from_user.id,
                                       'Готово. Данные загружены.',
                                       reply_markup=types.ReplyKeyboardRemove())
            omb_types.map_addfiles[addfile.omap_id] = omb_postgre.get_all_addfiles(addfile.omap_id)

            omap = omb_types.omap_dict[chat_id]
            if omap.telegram_file_type == 'photo':
                msg = omb_types.bot.send_photo(message.chat.id, omap.telegram_file_id, caption='-')
                omb_find_map.switch_map(msg.chat.id, msg.message_id, show_addfiles=True)
            elif omap.telegram_file_type == 'document':
                msg = omb_types.bot.send_document(message.chat.id, omap.telegram_file_id, caption='-')
                omb_find_map.switch_map(msg.chat.id, msg.message_id, show_addfiles=True)

        elif message.text == "Нет":
            omb_types.bot.send_message(message.from_user.id, 'Ну ок.', reply_markup=None)

    except Exception as e:
        omb_postgre.log_db('save_data_to_db', message.from_user.id, str(e))
        omb_types.bot.reply_to(message, omb_types.errors["omb-001"],
                               reply_markup=types.ReplyKeyboardRemove())
