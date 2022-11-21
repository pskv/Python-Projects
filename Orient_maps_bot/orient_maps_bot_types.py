import telebot
from telebot import types
import orient_maps_bot_postgre as omb_postgre


with open('Orient_maps_bot/telebot_token.txt') as f:
    bot_token = f.read().strip()
global bot
bot = telebot.TeleBot(bot_token)


class Omap:
    def __init__(self, name):
        self.name = name
        self.telegram_file_type = None
        self.location = None
        self.event_date = None
        self.tags = None
        self.owner = None
        self.index = None
        self.telegram_file_id = None
        self.id = None


omap_dict = {}    # текущая карта пользователя (экземпляр класса Omap)
map_pointer = {}  # кол-во карт в выборке и порядковый номер карты, выбранной пользователем в данный момент
user_maps = {}    # вся выборка карт пользователя


class Addfile:
    def __init__(self, omap_id, file_type):
        self.omap_id = omap_id
        self.file_type = file_type
        self.telegram_file_id = None
        self.file_id = None
        self.telegram_file_type = None


map_addfiles = {}  # все дополнительные файлы для выбранной карты


errors = {"omb-001": "Что-то пошло не так. Придётся начинать сначала.",
          "omb-002": "Не похоже на карту. Давай по новой.",
          "omb-003": "Не похоже на геолокацию. Давай по новой.",
          "omb-004": "Неправильный формат даты. Давай по новой."
          }


def welcome_keyboard(user_id):  # клавиатура главного меню
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Загрузить карту🗄', callback_data='upload_map'))
    if omb_postgre.check_maps_exist(user_id):
        keyboard.add(types.InlineKeyboardButton(text='Найти карту🔎', callback_data='find_map'))
    if user_id == 366436625:
        keyboard.add(types.InlineKeyboardButton(text='🕶Админка🕶', callback_data='admin_info'))
    return keyboard


def find_map_keyboard():  # клавиатура поиска карт
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Показать все🌍', callback_data='show_all'))
    keyboard.add(types.InlineKeyboardButton(text='Поиск по индексу🏷', callback_data='find_by_first_letter'))
    keyboard.add(types.InlineKeyboardButton(text='Поиск по хэштэгам#️⃣', callback_data='find_by_tags'))
    keyboard.add(types.InlineKeyboardButton(text='Поиск по геолокации📌', callback_data='find_by_geoloc'))
    keyboard.add(types.InlineKeyboardButton(text='Поиск по дате📅', callback_data='find_by_date'))
    keyboard.add(types.InlineKeyboardButton(text='↩️Назад в главное меню', callback_data='main_menu'))
    return keyboard


def map_switch_keyboard(keyboard_spec, addfile_cnt=0, show_addfiles=False, omap_id=0):  # клавиатура при выборе карт
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 5
    inline_buttons = []
    if keyboard_spec[0] > 1:
        k_button = types.InlineKeyboardButton(text='⏮ 1', callback_data='first_map')
        inline_buttons.append(k_button)
    if keyboard_spec[0] > 2:
        k_button = types.InlineKeyboardButton(text='◀ '+str(keyboard_spec[0]-1), callback_data='prev_map')
        inline_buttons.append(k_button)
    inline_buttons.append(types.InlineKeyboardButton(text='• '+str(keyboard_spec[0])+' •', callback_data='curr_map'))
    if keyboard_spec[1]-keyboard_spec[0] >= 2:
        k_button = types.InlineKeyboardButton(text=str(keyboard_spec[0]+1)+' ▶', callback_data='next_map')
        inline_buttons.append(k_button)
    if keyboard_spec[1]-keyboard_spec[0] >= 1:
        k_button = types.InlineKeyboardButton(text=str(keyboard_spec[1])+' ⏭', callback_data='last_map')
        inline_buttons.append(k_button)
    keyboard.add(*inline_buttons)  # добавляем кнопки в клавиатуру
    keyboard.add(types.InlineKeyboardButton(text='Геолокация📌', callback_data='show_geoloc'),
                 types.InlineKeyboardButton(text='Добавить файл📎', callback_data='add_file'))
    keyboard.add(types.InlineKeyboardButton(text='Редактировать✏️', callback_data='edit_map'),
                 types.InlineKeyboardButton(text='Удалить❌', callback_data='delete_map'))
    if addfile_cnt > 0:
        if not show_addfiles:
            keyboard.add(types.InlineKeyboardButton(text='⬇️Показать дополнительные файлы⬇️',
                                                    callback_data='show_addfiles'))
        else:
            keyboard.add(types.InlineKeyboardButton(text='⬇️Дополнительные файлы⬇️',
                                                    callback_data='hide_addfiles'))
            for file in map_addfiles[omap_id]:
                keyboard.add(types.InlineKeyboardButton(text=file[2], callback_data='show_addfile_'+str(file[0])))
            keyboard.add(types.InlineKeyboardButton(text='⬆️Скрыть дополнительные файлы⬆️',
                                                    callback_data='hide_addfiles'))
    keyboard.add(types.InlineKeyboardButton(text='↩️Назад в главное меню', callback_data='main_menu_from_maps'))
    return keyboard


def map_edit_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Заменить карту🗺', callback_data='edit_map_file'),
                 types.InlineKeyboardButton(text='Изменить дату📅', callback_data='edit_event_date'))
    keyboard.add(types.InlineKeyboardButton(text='Изменить хэштэги#️⃣', callback_data='edit_tags'),
                 types.InlineKeyboardButton(text='Изменить индекс🏷', callback_data='edit_first_letter'))
    keyboard.add(types.InlineKeyboardButton(text='Изменить геолокацию📌', callback_data='edit_geoloc'))
    keyboard.add(types.InlineKeyboardButton(text='↩️Назад к выбору карт', callback_data='map_switch_from_edit'))
    return keyboard


def return_to_map_switch():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='↩️Назад к выбору карт', callback_data='map_switch_from_addfile'))
    return keyboard


def return_to_map_switch_from_geoloc():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='↩️Назад к выбору карт', callback_data='map_switch_from_geoloc'))
    return keyboard


def show_stat_first_letter():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Посмотреть статистику', callback_data='show_stat_first_letter'))
    return keyboard


def show_stat_tags():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Посмотреть статистику', callback_data='show_stat_tags'))
    return keyboard


def map_delete_mode():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Выкинуть бумажную карту🗑', callback_data='delete_paper_map'))
    keyboard.add(types.InlineKeyboardButton(text='Удалить полностью❌', callback_data='delete_completely'))
    keyboard.add(types.InlineKeyboardButton(text='↩️Назад к выбору карт', callback_data='map_switch_from_edit'))
    return keyboard


def map_delete_paper_confirm():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Да', callback_data='delete_paper_map_yes'))
    keyboard.add(types.InlineKeyboardButton(text='Нет', callback_data='delete_paper_map_no'))
    return keyboard


def map_delete_completely_confirm():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Да', callback_data='delete_completely_yes'))
    keyboard.add(types.InlineKeyboardButton(text='Нет', callback_data='delete_completely_no'))
    return keyboard
