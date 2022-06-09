from telebot import types
import orient_maps_bot_types as omb_types
import orient_maps_bot_postgre as omb_postgre


def start(m, admin_mode=False):

    # Логирование обращений к боту
    username = ''
    if m.from_user.first_name is not None:
        username = m.from_user.first_name + ' '
    if m.from_user.last_name is not None:
        username += m.from_user.last_name
    omb_postgre.log_db('/start', m.from_user.id, username)

    # Проверка доступов
    if omb_postgre.check_access(m.from_user.id, username)[1] != 'ALLOWED':
        omb_types.bot.send_message(m.chat.id, 'Нет доступа.')
        return

    # приветственное сообщение из файла welcome_message.txt
    with open('Orient_maps_bot/welcome_message.txt', encoding='utf8') as wf:
        welcome_message = wf.read().strip()
    omb_types.bot.send_message(m.chat.id, welcome_message, reply_markup=types.ReplyKeyboardRemove())
    msg = omb_types.bot.send_message(chat_id=m.chat.id, text='Главное меню:', reply_markup=None)
    omb_types.bot.edit_message_reply_markup(m.chat.id, msg.message_id,
                                            reply_markup=omb_types.welcome_keyboard(admin_mode))


def description(m):
    with open('Orient_maps_bot/descrption.txt', encoding='utf8') as df:
        desc_message = df.read().strip()
    omb_types.bot.send_message(m.chat.id, desc_message, parse_mode='Markdown')
