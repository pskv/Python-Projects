
import telebot
from telebot import types
from datetime import date, timedelta

with open('telebot_token.txt') as f:
    bot_token = f.read()
# Создаем экземпляр бота
bot = telebot.TeleBot(bot_token)



map_dict = {}
class Map:
    def __init__(self, name):
        self.name = name
        self.content = None
        self.location = None
        self.event_date = None
        self.tags = None
        self.owner = None
        self.map_first_letter = None


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):

    # TODO Сделать логирование обращений к боту
    print(m.from_user.id, m.from_user.first_name, m.from_user.last_name)


    keyboard = types.InlineKeyboardMarkup();  # клавиатура
    key_yes = types.InlineKeyboardButton(text='Загрузить карту', callback_data='Upload');  # кнопка «Загрузить карту»
    keyboard.add(key_yes);  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Найти карту', callback_data='Find'); # кнопка «Найти карту»
    keyboard.add(key_no);
    bot.send_message(m.chat.id, 'Что будем делать?', reply_markup=keyboard)


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

        if message.content_type == 'document':
            file_name = message.document.file_name;
            file_info = bot.get_file(message.document.file_id)
        elif message.content_type == 'photo':
            file_name = message.photo[len(message.photo) - 1].file_id;
            file_info = bot.get_file(file_name)
            file_name += '.jpg'
        else:
            bot.reply_to(message, 'Не похоже на карту. Давай по новой.')
            bot.register_next_step_handler(message, Upload_map);
            return

        chat_id = message.chat.id
        map = Map(file_name)
        map.content = bot.download_file(file_info.file_path)
        map.owner = message.from_user.id
        map_dict[chat_id] = map

        # Сохранение файла на диск
        ####################
        # with open(file_name, 'wb') as new_file:
        #     new_file.write(map.content)
        #####################

        bot.reply_to(message, 'Файл загружен')

        bot.send_message(message.from_user.id, 'Теперь нужны координаты (приложи геолокацию)')
        bot.register_next_step_handler(message, Get_location);  # следующий шаг – функция Get_location
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так. Придётся начинать сначала')

def Get_location(message): #получаем координаты
    try:
        if message.content_type != 'location':
            bot.reply_to(message, 'Не похоже на геолокацию. Давай по новой.')
            bot.register_next_step_handler(message, Get_location);
            return

        location_long = message.location.longitude;
        location_lat = message.location.latitude;

        chat_id = message.chat.id
        map = map_dict[chat_id]
        map.location = {'longitude': location_long, 'latitude': location_lat}

        bot.reply_to(message, 'Координаты загружены')

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("Сегодня", "Вчера")
        bot.send_message(message.from_user.id, "Когда был старт? (укажи дату в формате YYYY-MM-DD)", reply_markup=markup)

        bot.register_next_step_handler(message, Get_event_date);  # следующий шаг – функция Get_event_date
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так. Придётся начинать сначала')

def Get_event_date(message): #получаем дату
    try:
        event_date = message.text;
        if event_date == 'Сегодня':
            event_date = date.today()
        elif event_date == 'Вчера':
            event_date = date.today() - timedelta(days=1)

        chat_id = message.chat.id
        map = map_dict[chat_id]
        map.event_date = event_date

        bot.reply_to(message, 'Дата загружена', reply_markup=types.ReplyKeyboardRemove())

        bot.send_message(message.from_user.id, "Укажи хэштэги")
        bot.register_next_step_handler(message, Get_tags);  # следующий шаг – функция Get_tags
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так. Придётся начинать сначала')

def Get_tags(message): #получаем хэштэги
    try:
        tags = message.text;

        chat_id = message.chat.id
        map = map_dict[chat_id]
        map.tags = tags

        bot.reply_to(message, 'Хэштэги загружены')

        bot.send_message(message.from_user.id, "Укажи первую букву названия карты")
        bot.register_next_step_handler(message, Get_first_letter);  # следующий шаг – функция Get_first_letter
    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так. Придётся начинать сначала')

def Get_first_letter(message): #получаем первую букву названия карты
    try:
        map_first_letter = message.text;

        chat_id = message.chat.id
        map = map_dict[chat_id]
        map.map_first_letter = map_first_letter

        bot.reply_to(message, 'Загружено')

        bot.send_message(message.from_user.id, 'Вот что получилось: \n ~~~~~~~~~~~~~~ \nКарта загружена.' + '\n'
                         + 'Координаты: ' + str(map.location['longitude']) + ', ' + str(map.location['latitude']) + '\n'
                         + 'Дата: ' + str(map.event_date) + '\n'
                         + 'Хэштэги: ' + map.tags + '\n'
                         + 'Первая буква названия: ' + map.map_first_letter + '\n'
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
        # map = map_dict[chat_id]

    except Exception as e:
        bot.reply_to(message, 'Что-то пошло не так. Придётся начинать сначала')

# Запускаем бота
bot.polling(none_stop=True, interval=0)