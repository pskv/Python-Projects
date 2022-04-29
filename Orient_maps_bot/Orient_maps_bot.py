import telebot
from telebot import types
from datetime import date, timedelta, datetime, timezone
import validators
import psycopg2

with open('Orient_maps_bot/telebot_token.txt') as f:
    bot_token = f.read().strip()
# Создаем экземпляр бота
bot = telebot.TeleBot(bot_token)

with open('Orient_maps_bot/postgre_params.txt') as f:
    postgre_params_raw = f.read().strip()
postgre_params = dict()
for param in postgre_params_raw.split('\n'):
    postgre_params[param.split(':')[0]] = param.split(':')[1]

omap_dict = {}


class Omap:
    def __init__(self, name):
        self.name = name
        self.omap_type = None
        self.location = None
        self.event_date = None
        self.tags = None
        self.owner = None
        self.omap_first_letter = None
        self.telegram_file_id = None


curr_omap = {}
user_maps = {}


def log_db(oper, user_id, comment):  # Логирование
    conn = psycopg2.connect(dbname=postgre_params['dbname'], user=postgre_params['user'],
                            password=postgre_params['password'], host=postgre_params['host'])

    with conn.cursor() as cursor:
        insert = 'INSERT INTO ' + postgre_params['log_table'] + ' (tmst,oper,user_id,comment) VALUES (%s, %s, %s, %s)'
        cursor.execute(insert, (datetime.now(timezone.utc), oper, user_id, comment))
        conn.commit()
        cursor.close()
    conn.close()


# Функция проверки доступов (по умолчанию доступ есть у всех, но его можно забрать у конкретных пользователей)
def check_access(user_id, username):
    conn = psycopg2.connect(dbname=postgre_params['dbname'], user=postgre_params['user'],
                            password=postgre_params['password'], host=postgre_params['host'])
    with conn.cursor() as cursor:
        cursor.execute('SELECT user_id,access_mode '
                       'FROM ' + postgre_params['users_table'] +
                       ' where user_id = %s', (user_id,))
        record = cursor.fetchone()
        cursor.close()
    conn.close()
    if record:  # Если пользователь уже есть, то возвращаем его доступ
        return record
    else:  # Если пользователя нет, то добавляем его и предоставляем доступ
        conn = psycopg2.connect(dbname=postgre_params['dbname'],
                                user=postgre_params['user'],
                                password=postgre_params['password'],
                                host=postgre_params['host'])
        with conn.cursor() as cursor:
            insert = 'INSERT INTO ' + postgre_params['users_table'] +\
                     ' (user_id, username, access_mode) VALUES (%s, %s, %s)'
            cursor.execute(insert, (user_id, username, 'ALLOWED'))
            conn.commit()
            cursor.close()
        conn.close()
        log_db('first_login', user_id, None)
        return user_id, 'ALLOWED'


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m):

    # Логирование обращений к боту
    username = ''
    if m.from_user.first_name is not None:
        username = m.from_user.first_name + ' '
    if m.from_user.last_name is not None:
        username += m.from_user.last_name
    log_db('/start', m.from_user.id, username)

    # Проверка доступов
    if check_access(m.from_user.id, username)[1] != 'ALLOWED':
        bot.send_message(m.chat.id, 'Нет доступа.')
        return

    # приветственное сообщение из файла welcome_message.txt
    with open('Orient_maps_bot/welcome_message.txt', encoding='utf8') as wf:
        welcome_message = wf.read().strip()
    bot.send_message(m.chat.id, welcome_message)


@bot.message_handler(commands=["welcome"])
def upload_map_cmd(message):
    with open('Orient_maps_bot/descrption.txt', encoding='utf8') as df:
        desc_message = df.read().strip()
    bot.send_message(message.chat.id, desc_message, parse_mode='Markdown')


# Функция, обрабатывающая команду /modify_user
@bot.message_handler(commands=["modify_user"])
def modify_user(message):
    if message.from_user.id != 366436625:
        bot.send_message(message.chat.id, 'Чтобы начать напиши /start')
        return
    if message.text == '/modify_user':
        bot.send_message(message.chat.id, 'Это команда для изменения прав пользователя\n\n'
                                          '-all - показать всех пользователей\n'
                                          '/modify_user user_id access_mode - поменять пользоватлю user_id права')
    elif message.text.split()[1] == '-all':
        conn = psycopg2.connect(dbname=postgre_params['dbname'],
                                user=postgre_params['user'],
                                password=postgre_params['password'],
                                host=postgre_params['host'])
        with conn.cursor() as cursor:
            cursor.execute('SELECT user_id,username,access_mode FROM ' + postgre_params['users_table'])
            records = cursor.fetchall()
            bot.send_message(message.chat.id, '\n'.join([str(row[0])+' - '+row[1]+' - '+row[2] for row in records]))
            cursor.close()
        conn.close()
    elif len(message.text.split()) == 3:
        if message.text.split()[2] not in ['ALLOWED', 'DENIED']:
            bot.send_message(message.chat.id, 'Поддерживаются только режимы доступа ALLOWED и DENIED')
            return
        conn = psycopg2.connect(dbname=postgre_params['dbname'],
                                user=postgre_params['user'],
                                password=postgre_params['password'],
                                host=postgre_params['host'])
        with conn.cursor() as cursor:
            update = 'UPDATE ' + postgre_params['users_table'] + ' set ACCESS_MODE = %s where user_id = %s'
            cursor.execute(update, (message.text.split()[2], message.text.split()[1]))
            conn.commit()
            cursor.close()
        conn.close()
        log_db('/modify_user', message.from_user.id,
               'affected user_id: '+message.text.split()[1]+' access_mode: '+message.text.split()[2])
        bot.send_message(message.chat.id, 'Готово')


# Обработка inline кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "first_map":  # call.data это callback_data, которую мы указали при объявлении кнопки
        curr_omap[call.message.chat.id][0] = 1
        switch_map(call.message.chat.id, call.message.message_id)
    elif call.data == "prev_map":
        curr_omap[call.message.chat.id][0] -= 1
        switch_map(call.message.chat.id, call.message.message_id)
    elif call.data == "next_map":
        curr_omap[call.message.chat.id][0] += 1
        switch_map(call.message.chat.id, call.message.message_id)
    elif call.data == "last_map":
        curr_omap[call.message.chat.id][0] = curr_omap[call.message.chat.id][1]
        switch_map(call.message.chat.id, call.message.message_id)


def switch_map(user_id, message_id):
    if user_maps[user_id][curr_omap[user_id][0]-1][2] == 'photo':
        bot.edit_message_media(types.InputMediaPhoto(user_maps[user_id][curr_omap[user_id][0]-1][5]),
                               user_id, message_id)
    elif user_maps[user_id][curr_omap[user_id][0]-1][2] == 'document':
        bot.edit_message_media(types.InputMediaDocument(user_maps[user_id][curr_omap[user_id][0] - 1][5]),
                               user_id, message_id)
    bot.edit_message_caption('Дата: ' + str(user_maps[user_id][curr_omap[user_id][0]-1][3]) + '\n' +
                             user_maps[user_id][curr_omap[user_id][0]-1][4] + '\n' +
                             'Карта лежит в файле с буквой "' + user_maps[user_id][curr_omap[user_id][0]-1][6] +
                             '" под номером ' + str(user_maps[user_id][curr_omap[user_id][0]-1][7]),
                             user_id, message_id)
    bot.edit_message_reply_markup(user_id, message_id, reply_markup=map_switch_keyboard(curr_omap[user_id]))


@bot.message_handler(commands=["upload_map"])
def upload_map_cmd(message):
    bot.send_message(message.chat.id, 'Давай её сюда')
    bot.register_next_step_handler(message, upload_map)  # следующий шаг – функция upload_map


def map_switch_keyboard(keyboard_spec):
    keyboard = types.InlineKeyboardMarkup()  # клавиатура
    keyboard.row_width = 5
    inline_buttons = []
    if keyboard_spec[0] > 1:
        k_button = types.InlineKeyboardButton(text='<< 1', callback_data='first_map')
        inline_buttons.append(k_button)
    if keyboard_spec[0] > 2:
        k_button = types.InlineKeyboardButton(text='< '+str(keyboard_spec[0]-1), callback_data='prev_map')
        inline_buttons.append(k_button)
    inline_buttons.append(types.InlineKeyboardButton(text='• '+str(keyboard_spec[0])+' •', callback_data='curr_map'))
    if keyboard_spec[1]-keyboard_spec[0] >= 2:
        k_button = types.InlineKeyboardButton(text='> '+str(keyboard_spec[0]+1), callback_data='next_map')
        inline_buttons.append(k_button)
    if keyboard_spec[1]-keyboard_spec[0] >= 1:
        k_button = types.InlineKeyboardButton(text='>> '+str(keyboard_spec[1]), callback_data='last_map')
        inline_buttons.append(k_button)
    keyboard.add(*inline_buttons)  # добавляем кнопки в клавиатуру
    return keyboard


@bot.message_handler(commands=["show_last_map"])
def show_last_map_cmd(message):

    user_id = message.chat.id
    conn = psycopg2.connect(dbname=postgre_params['dbname'],
                            user=postgre_params['user'],
                            password=postgre_params['password'],
                            host=postgre_params['host'])
    with conn.cursor() as cursor:
        cursor.execute('SELECT omap_id,name,omap_type,event_date,tags,telegram_file_id, '
                       'omap_first_letter,row_number() over(partition by omap_first_letter order by omap_id) as omap_letter_seq '
                       'FROM ' + postgre_params['maps_table'] + ' where owner = %s order by omap_id',
                       (user_id,))
        records = cursor.fetchall()
        cursor.close()
    conn.close()
    if len(records) == 0:
        bot.send_message(message.chat.id, 'Похоже пока нет ни одной карты.')
        return
    curr_omap[user_id] = [len(records),  # сохраняем кол-во карт
                          len(records)]  # номер последней карты
    user_maps[user_id] = records

    if records[-1][2] == 'document':
        bot.send_document(message.chat.id, records[-1][5],
                          caption='Дата: ' + str(records[-1][3]) + '\n' + records[-1][4] + '\n' +
                                  'Карта лежит в файле с буквой "' + records[-1][6] + '" под номером ' + str(records[-1][7]),
                          reply_markup=map_switch_keyboard(curr_omap[user_id])
                          )
    elif records[-1][2] == 'photo':
        bot.send_photo(message.chat.id, records[-1][5],
                       caption='Дата: ' + str(records[-1][3]) + '\n' + records[-1][4] + '\n' +
                                  'Карта лежит в файле с буквой "' + records[-1][6] + '" под номером ' + str(records[-1][7]),
                       reply_markup=map_switch_keyboard(curr_omap[user_id])
                       )


@bot.message_handler(commands=["find_map"])
def find_map_cmd(message):
    user_id = message.chat.id
    conn = psycopg2.connect(dbname=postgre_params['dbname'],
                            user=postgre_params['user'],
                            password=postgre_params['password'],
                            host=postgre_params['host'])
    with conn.cursor() as cursor:
        cursor.execute('SELECT name,omap_type,event_date,tags,telegram_file_id '
                       'FROM ' + postgre_params['maps_table'] + ' where owner = %s order by omap_id desc',
                       (user_id,))
        records = cursor.fetchall()
        cursor.close()
    conn.close()
    bot.send_message(message.chat.id,
                     'Всего карт загружено: ' + str(len(records)) + '\nПоиск пока в стадии разработки')


def upload_map(message):  # получаем карту
    # noinspection PyBroadException
    try:
        telegram_file_id = ''
        if message.text == '/start':
            start(message)
            return
        elif message.content_type == 'document':
            omap_type = 'document'
            file_name = message.document.file_name
            telegram_file_id = message.document.file_id
        elif message.content_type == 'photo':
            omap_type = 'photo'
            file_name = message.photo[len(message.photo) - 1].file_id
            telegram_file_id = message.photo[len(message.photo) - 1].file_id
        elif message.content_type == 'text' and validators.url(message.text):
            omap_type = 'url'
            file_name = message.text
            bot.reply_to(message, 'Похоже на URL. Ладно, пойдёт.')
        else:
            bot.reply_to(message, 'Не похоже на карту. Давай по новой.')
            bot.register_next_step_handler(message, upload_map)
            return

        chat_id = message.chat.id
        omap = Omap(file_name)
        omap.omap_type = omap_type
        if omap_type == 'url':
            omap.telegram_file_id = message.text
        else:
            omap.telegram_file_id = telegram_file_id
        omap.owner = message.from_user.id
        omap_dict[chat_id] = omap

        bot.reply_to(message, 'Файл загружен')
        bot.send_message(message.from_user.id, 'Теперь нужны координаты (приложи геолокацию)')
        bot.register_next_step_handler(message, get_location)  # следующий шаг – функция Get_location
    except Exception:
        bot.reply_to(message, 'Что-то пошло не так. Придётся начинать сначала')


def get_location(message):  # получаем координаты
    # noinspection PyBroadException
    try:
        if message.text == '/start':
            start(message)
            return
        elif message.content_type != 'location':
            bot.reply_to(message, 'Не похоже на геолокацию. Давай по новой.')
            bot.register_next_step_handler(message, get_location)
            return

        location_long = message.location.longitude
        location_lat = message.location.latitude

        chat_id = message.chat.id
        omap = omap_dict[chat_id]
        omap.location = {'longitude': location_long, 'latitude': location_lat}

        bot.reply_to(message, 'Координаты загружены')

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("Сегодня", "Вчера")
        bot.send_message(message.from_user.id,
                         "Когда был старт? (укажи дату в формате YYYY-MM-DD)",
                         reply_markup=markup)

        bot.register_next_step_handler(message, get_event_date)  # следующий шаг – функция Get_event_date
    except Exception:
        bot.reply_to(message, 'Что-то пошло не так. Придётся начинать сначала')


def get_event_date(message):  # получаем дату
    # noinspection PyBroadException
    try:
        if message.text == '/start':
            start(message)
            return

        event_date = message.text
        if event_date == 'Сегодня':
            event_date = date.today()
        elif event_date == 'Вчера':
            event_date = date.today() - timedelta(days=1)
        else:
            try:
                event_date = datetime.strptime(event_date, '%Y-%m-%d').date()
            except ValueError:
                bot.reply_to(message, 'Неправильный формат даты. Давай по новой.')
                bot.register_next_step_handler(message, get_event_date)
                return

        chat_id = message.chat.id
        omap = omap_dict[chat_id]
        omap.event_date = event_date

        bot.reply_to(message, 'Дата загружена', reply_markup=types.ReplyKeyboardRemove())

        bot.send_message(message.from_user.id, "Укажи хэштэги")
        bot.register_next_step_handler(message, get_tags)  # следующий шаг – функция Get_tags
    except Exception:
        bot.reply_to(message, 'Что-то пошло не так. Придётся начинать сначала')


def get_tags(message):  # получаем хэштэги
    # noinspection PyBroadException
    try:
        if message.text == '/start':
            start(message)
            return

        tags = message.text

        if len(list(filter(lambda x: x != '#', map(lambda x: x[0], tags.split())))) > 0:
            bot.reply_to(message, 'Все хэштэги должны начинаться с символа #. Давай по новой.')
            bot.register_next_step_handler(message, get_tags)
            return

        if len(list(filter(lambda x: x == 0, map(lambda x: len(x[1:]), tags.split())))) > 0:
            bot.reply_to(message, 'Путые хэштэги запрещены. Давай по новой.')
            bot.register_next_step_handler(message, get_tags)
            return

        if len(tags.split()) != len(set(tags.split())):
            bot.reply_to(message, 'Ладно, дубли сам удалю.')
            tags = ' '.join(set(tags.split()))

        chat_id = message.chat.id
        omap = omap_dict[chat_id]
        omap.tags = tags

        bot.reply_to(message, 'Хэштэги загружены')

        bot.send_message(message.from_user.id, "Укажи первую букву названия карты")
        bot.register_next_step_handler(message, get_first_letter)  # следующий шаг – функция Get_first_letter
    except Exception:
        bot.reply_to(message, 'Что-то пошло не так. Придётся начинать сначала')


def get_first_letter(message):  # получаем первую букву названия карты
    # noinspection PyBroadException
    try:
        if message.text == '/start':
            start(message)
            return
        omap_first_letter = message.text
        if len(omap_first_letter) > 1 or not omap_first_letter.isalpha():
            bot.reply_to(message, 'Надо одну букву. Давай по новой.')
            bot.register_next_step_handler(message, get_first_letter)
            return

        chat_id = message.chat.id
        omap = omap_dict[chat_id]
        omap.omap_first_letter = omap_first_letter

        bot.reply_to(message, 'Загружено')

        bot.send_message(message.from_user.id, 'Вот что получилось: \n ~~~~~~~~~~~~~~ \nКарта загружена.' + '\n'
                         + 'Координаты: ' + str(omap.location['longitude']) + ', ' +
                         str(omap.location['latitude']) + '\n'
                         + 'Дата: ' + str(omap.event_date) + '\n'
                         + 'Хэштэги: ' + omap.tags + '\n'
                         + 'Первая буква названия: ' + omap.omap_first_letter + '\n'
                         + '~~~~~~~~~~~~~~ \n'
                         )
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("Да", "Нет")
        bot.send_message(message.from_user.id, "Сохраняем?", reply_markup=markup)

        bot.register_next_step_handler(message, save_data_to_db)  # следующий шаг – функция Save_data_to_db

    except Exception:
        bot.reply_to(message, 'Что-то пошло не так. Придётся начинать сначала')


def save_data_to_db(message):
    # noinspection PyBroadException
    try:
        if message.text == "Да":
            chat_id = message.chat.id
            omap = omap_dict[chat_id]
            conn = psycopg2.connect(dbname=postgre_params['dbname'], user=postgre_params['user'],
                                    password=postgre_params['password'], host=postgre_params['host'])
            with conn.cursor() as cursor:
                insert = 'INSERT INTO ' + postgre_params['maps_table'] + \
                         ' (name,omap_type,longitude,latitude,event_date,' \
                         'tags,owner,omap_first_letter,telegram_file_id) ' \
                         'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) '
                cursor.execute(insert, (omap.name, omap.omap_type,
                                        omap.location['longitude'], omap.location['latitude'],
                                        omap.event_date, omap.tags, omap.owner, omap.omap_first_letter,
                                        omap.telegram_file_id))
                conn.commit()
                select = 'select count(1) ' \
                         '  from orient_maps_bot.maps t ' \
                         ' where owner = %s ' \
                         'and omap_first_letter = %s'
                cursor.execute(select, (omap.owner, omap.omap_first_letter))
                cnt = cursor.fetchone()
                cursor.close()

            conn.close()
            bot.send_message(message.from_user.id,
                             'Готово. Данные загружены в БД.\n'
                             'Карту нужно убрать в файл с буквой "' + omap.omap_first_letter + '"\n'
                             'Номер этой карты в файле: ' + str(cnt[0]),
                             reply_markup=types.ReplyKeyboardRemove())

        elif message.text == "Нет":
            bot.send_message(message.from_user.id, 'Ну ок.', reply_markup=types.ReplyKeyboardRemove())

    except Exception as e:
        log_db('save_data_to_db', message.from_user.id , str(e))
        bot.reply_to(message, 'Что-то пошло не так. Придётся начинать сначала')


# Получение любых сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    start(message)


# Запускаем бота
# bot.polling(none_stop=True, interval=0)
bot.infinity_polling()
