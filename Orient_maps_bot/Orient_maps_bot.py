import telebot
from telebot import types
from datetime import date, timedelta, datetime, timezone
import validators
import psycopg2

with open('telebot_token.txt') as f:
    bot_token = f.read()
# Создаем экземпляр бота
bot = telebot.TeleBot(bot_token)

with open('postgre_params.txt') as f:
    postgre_params_raw = f.read()
postgre_params = dict()
for param in postgre_params_raw.split('\n'):
    postgre_params[param.split(':')[0]] = param.split(':')[1]

omap_dict = {}
class Omap:
    def __init__(self, name):
        self.name = name
        self.omap_type = None
        self.content = None
        self.location = None
        self.event_date = None
        self.tags = None
        self.owner = None
        self.omap_first_letter = None


def log_db(oper, username, comment):  # Логирование
    conn = psycopg2.connect(dbname=postgre_params['dbname'], user=postgre_params['user'], password=postgre_params['password'], host=postgre_params['host'])

    with conn.cursor() as cursor:
        insert = 'INSERT INTO ' + postgre_params['log_table'] + ' (tmst,oper,username,comment) VALUES (%s, %s, %s, %s)'
        cursor.execute(insert, (datetime.now(timezone.utc), oper, username, comment))
        conn.commit()
        cursor.close()
    conn.close()

def check_access(user_id, username):  # Проверка доступа
    conn = psycopg2.connect(dbname=postgre_params['dbname'], user=postgre_params['user'], password=postgre_params['password'], host=postgre_params['host'])
    with conn.cursor() as cursor:
        cursor.execute('SELECT user_id,access_mode FROM ' + postgre_params['users_table'] + ' where user_id = %s', (user_id,))
        record = cursor.fetchone()
        cursor.close()
    conn.close()
    if record:
        return record
    else:
        conn = psycopg2.connect(dbname=postgre_params['dbname'], user=postgre_params['user'], password=postgre_params['password'], host=postgre_params['host'])
        with conn.cursor() as cursor:
            insert = 'INSERT INTO ' + postgre_params['users_table'] + ' (user_id, username, access_mode) VALUES (%s, %s, %s)'
            cursor.execute(insert, (user_id, username, 'NEW'))
            conn.commit()
            cursor.close()
        conn.close()
        return (user_id, 'NEW')

# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):

    # Логирование обращений к боту
    if m.from_user.first_name is not None:
        username = m.from_user.first_name + ' '
    if m.from_user.last_name is not None:
        username += m.from_user.last_name
    log_db('/start', m.from_user.id, username)


    # Проверка доступов
    if check_access(m.from_user.id, username)[1] != 'ALLOWED':
        bot.send_message(m.chat.id, 'Нет доступа. Сорян.')
        return


    keyboard = types.InlineKeyboardMarkup();  # клавиатура
    key_yes = types.InlineKeyboardButton(text='Загрузить карту', callback_data='Upload');  # кнопка «Загрузить карту»
    keyboard.add(key_yes);  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Найти карту', callback_data='Find'); # кнопка «Найти карту»
    keyboard.add(key_no);
    bot.send_message(m.chat.id, 'Что будем делать?', reply_markup=keyboard)


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
        conn = psycopg2.connect(dbname=postgre_params['dbname'], user=postgre_params['user'], password=postgre_params['password'], host=postgre_params['host'])
        with conn.cursor() as cursor:
            cursor.execute('SELECT user_id,username,access_mode FROM ' + postgre_params['users_table'])
            records = cursor.fetchall()
            bot.send_message(message.chat.id, '\n'.join([str(row[0])+' - '+row[1]+' - '+row[2] for row in records]))
            cursor.close()
        conn.close()
    elif len(message.text.split()) == 3:
        if message.text.split()[2] not in ['ALLOWED','DENIED']:
            bot.send_message(message.chat.id, 'Поддерживаются только режимы доступа ALLOWED и DENIED')
            return
        conn = psycopg2.connect(dbname=postgre_params['dbname'], user=postgre_params['user'], password=postgre_params['password'], host=postgre_params['host'])
        with conn.cursor() as cursor:
            update = 'UPDATE ' + postgre_params['users_table'] + ' set ACCESS_MODE = %s where user_id = %s'
            cursor.execute(update, (message.text.split()[2], message.text.split()[1]))
            conn.commit()
            cursor.close()
        conn.close()
        bot.send_message(message.chat.id, 'Готово')


         # Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, 'Чтобы начать напиши /start')


# Обработка кнопки выбора действия
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "Upload": #call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.message.chat.id, 'Давай её сюда');
        bot.register_next_step_handler(call.message, Upload_map);  # следующий шаг – функция Upload_map
    elif call.data == "Find":
        bot.send_message(call.message.chat.id, 'Ща найду');
        bot.send_message(call.message.chat.id, 'А, ой. Пока не могу');

def Upload_map(message): #получаем карту
    try:
        if message.text == '/start':
            start(message, res=False)
            return
        elif message.content_type == 'document':
            omap_type = 'document'
            file_name = message.document.file_name;
            file_info = bot.get_file(message.document.file_id)
        elif message.content_type == 'photo':
            omap_type = 'photo'
            file_name = message.photo[len(message.photo) - 1].file_id;
            file_info = bot.get_file(file_name)
            file_name += '.jpg'
        elif message.content_type == 'text' and validators.url(message.text):
            omap_type = 'url'
            file_name = message.text
            bot.reply_to(message, 'Похоже на URL. Ладно, пойдёт.')
        else:
            bot.reply_to(message, 'Не похоже на карту. Давай по новой.')
            bot.register_next_step_handler(message, Upload_map);
            return

        chat_id = message.chat.id
        omap = Omap(file_name)
        omap.omap_type = omap_type
        if omap_type == 'url':
            omap.content = message.text
        else:
            omap.content = bot.download_file(file_info.file_path)
        omap.owner = message.from_user.id
        omap_dict[chat_id] = omap

        # Сохранение файла на диск
        ####################
        # with open(file_name, 'wb') as new_file:
        #     new_file.write(omap.content)
        #####################

        bot.reply_to(message, 'Файл загружен')

        bot.send_message(message.from_user.id, 'Теперь нужны координаты (приложи геолокацию)')
        bot.register_next_step_handler(message, Get_location);  # следующий шаг – функция Get_location
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так. Придётся начинать сначала')

def Get_location(message): #получаем координаты
    try:
        if message.text == '/start':
            start(message, res=False)
            return
        elif message.content_type != 'location':
            bot.reply_to(message, 'Не похоже на геолокацию. Давай по новой.')
            bot.register_next_step_handler(message, Get_location);
            return

        location_long = message.location.longitude;
        location_lat = message.location.latitude;

        chat_id = message.chat.id
        omap = omap_dict[chat_id]
        omap.location = {'longitude': location_long, 'latitude': location_lat}

        bot.reply_to(message, 'Координаты загружены')

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("Сегодня", "Вчера")
        bot.send_message(message.from_user.id, "Когда был старт? (укажи дату в формате YYYY-MM-DD)", reply_markup=markup)

        bot.register_next_step_handler(message, Get_event_date);  # следующий шаг – функция Get_event_date
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так. Придётся начинать сначала')

def Get_event_date(message): #получаем дату
    try:
        if message.text == '/start':
            start(message, res=False)
            return

        event_date = message.text;
        if event_date == 'Сегодня':
            event_date = date.today()
        elif event_date == 'Вчера':
            event_date = date.today() - timedelta(days=1)
        else:
            try:
                event_date = datetime.strptime(event_date, '%Y-%m-%d').date()
            except ValueError:
                bot.reply_to(message, 'Неправильный формат даты. Давай по новой.')
                bot.register_next_step_handler(message, Get_event_date);
                return

        chat_id = message.chat.id
        omap = omap_dict[chat_id]
        omap.event_date = event_date

        bot.reply_to(message, 'Дата загружена', reply_markup=types.ReplyKeyboardRemove())

        bot.send_message(message.from_user.id, "Укажи хэштэги")
        bot.register_next_step_handler(message, Get_tags);  # следующий шаг – функция Get_tags
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так. Придётся начинать сначала')

def Get_tags(message): #получаем хэштэги
    try:
        if message.text == '/start':
            start(message, res=False)
            return

        tags = message.text;

        if len(list(filter(lambda x: x != '#', map(lambda x: x[0], tags.split())))) > 0:
            bot.reply_to(message, 'Все хэштэги должны начинаться с символа #. Давай по новой.')
            bot.register_next_step_handler(message, Get_tags);
            return

        if len(list(filter(lambda x: x==0, map(lambda x: len(x[1:]), tags.split())))) > 0:
            bot.reply_to(message, 'Путые хэштэги запрещены. Давай по новой.')
            bot.register_next_step_handler(message, Get_tags);
            return

        if len(tags.split()) != len(set(tags.split())):
            bot.reply_to(message, 'Ладно, дубли сам удалю.')
            tags = ' '.join(set(tags.split()))


        chat_id = message.chat.id
        omap = omap_dict[chat_id]
        omap.tags = tags

        bot.reply_to(message, 'Хэштэги загружены')

        bot.send_message(message.from_user.id, "Укажи первую букву названия карты")
        bot.register_next_step_handler(message, Get_first_letter);  # следующий шаг – функция Get_first_letter
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так. Придётся начинать сначала')

def Get_first_letter(message): #получаем первую букву названия карты
    try:
        if message.text == '/start':
            start(message, res=False)
            return
        omap_first_letter = message.text;
        if len(omap_first_letter) > 1 or not omap_first_letter.isalpha():
            bot.reply_to(message, 'Надо одну букву. Давай по новой.')
            bot.register_next_step_handler(message, Get_first_letter);
            return

        chat_id = message.chat.id
        omap = omap_dict[chat_id]
        omap.omap_first_letter = omap_first_letter

        bot.reply_to(message, 'Загружено')

        bot.send_message(message.from_user.id, 'Вот что получилось: \n ~~~~~~~~~~~~~~ \nКарта загружена.' + '\n'
                         + 'Координаты: ' + str(omap.location['longitude']) + ', ' + str(omap.location['latitude']) + '\n'
                         + 'Дата: ' + str(omap.event_date) + '\n'
                         + 'Хэштэги: ' + omap.tags + '\n'
                         + 'Первая буква названия: ' + omap.omap_first_letter + '\n'
                         + '~~~~~~~~~~~~~~ \n'
                         )
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("Да", "Нет")
        bot.send_message(message.from_user.id, "Сохраняем?", reply_markup=markup)

        bot.register_next_step_handler(message, Save_data_to_db);  # следующий шаг – функция Save_data_to_db

    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так. Придётся начинать сначала')

def Save_data_to_db(message):
    try:
        if message.text == "Да":
            bot.send_message(message.from_user.id, 'Пока всё. Нужно писать загрузку в БД.', reply_markup=types.ReplyKeyboardRemove())
        elif message.text == "Нет":
            bot.send_message(message.from_user.id, 'Ну ок.', reply_markup=types.ReplyKeyboardRemove())

        # chat_id = message.chat.id
        # omap = omap_dict[chat_id]

    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так. Придётся начинать сначала')

# Запускаем бота
bot.polling(none_stop=True, interval=0)