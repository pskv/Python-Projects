import orient_maps_bot_types as omb_types
import orient_maps_bot_start as omb_start
import orient_maps_bot_upload_map as omb_upload_map
import orient_maps_bot_find_map as omb_find_map
import orient_maps_bot_postgre as omb_postgre
import orient_maps_bot_edit_map as omb_edit_map


# Обработка inline кнопок
@omb_types.bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "upload_map":
        omb_types.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        omb_types.bot.send_message(call.message.chat.id, '*Приложи карту.*', parse_mode='Markdown')
        omb_types.bot.register_next_step_handler(call.message, omb_upload_map.upload_map)
    elif call.data == "find_map":
        omb_types.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                                reply_markup=omb_types.find_map_keyboard())
    elif call.data == "main_menu":
        omb_types.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                                reply_markup=omb_types.welcome_keyboard
                                                (call.message.chat.id == 366436625))
    elif call.data == "main_menu_from_maps":
        omb_types.bot.send_message(call.message.chat.id, 'Возвращаемся в главное меню',
                                   reply_markup=omb_types.welcome_keyboard(call.message.chat.id == 366436625))
    elif call.data == "edit_map":
        omb_types.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                                reply_markup=omb_types.map_edit_keyboard())
    elif call.data == "add_file":
        omb_upload_map.add_file_cmd(call.message)
    elif call.data == "map_switch_from_edit":
        omb_types.bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=omb_types.map_switch_keyboard(
                omb_types.map_pointer[call.message.chat.id],
                omb_types.user_maps[call.message.chat.id][omb_types.map_pointer[call.message.chat.id][0]-1][10]))
    elif call.data == "show_all":
        omb_types.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        omb_find_map.show_all(call.message)
    elif call.data == "find_by_first_letter":
        omb_types.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        omb_types.bot.send_message(call.message.chat.id, '*Напиши букву*', parse_mode='Markdown',
                                   reply_markup=omb_types.show_stat_first_letter())
        omb_types.bot.register_next_step_handler(call.message, omb_find_map.find_by_first_letter)
    elif call.data == "show_stat_first_letter":
        omb_types.bot.send_message(
            call.message.chat.id,
            '\n'.join(["'" + str(row[0]) + "' - " + str(row[1])
                       for row in omb_postgre.get_stat_first_letter(call.message.chat.id)]))
        omb_types.bot.send_message(call.message.chat.id, '*Напиши букву*', parse_mode='Markdown',
                                   reply_markup=omb_types.show_stat_first_letter())

    elif call.data == "find_by_tags":
        omb_types.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        omb_types.bot.send_message(call.message.chat.id, '*Напиши хэштэг*', parse_mode='Markdown',
                                   reply_markup=omb_types.show_stat_tags())
        omb_types.bot.register_next_step_handler(call.message, omb_find_map.find_by_tags)
    elif call.data == "show_stat_tags":
        omb_types.bot.send_message(
            call.message.chat.id,
            '\n'.join([str(row[1]) + " - " + str(row[0])
                       for row in omb_postgre.get_stat_tags(call.message.chat.id)]))
        omb_types.bot.send_message(call.message.chat.id, '*Напиши хэштэг*', parse_mode='Markdown',
                                   reply_markup=omb_types.show_stat_tags())
    elif call.data == "find_by_geoloc":
        omb_types.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        omb_types.bot.send_message(call.message.chat.id, '*Приложи геолокацию*', parse_mode='Markdown')
        omb_types.bot.register_next_step_handler(call.message, omb_find_map.find_by_geoloc)
    elif call.data == "find_by_date":
        omb_types.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        omb_types.bot.send_message(call.message.chat.id, 'Укажи дату в формате *DD.MM.YYYY*', parse_mode='Markdown')
        omb_types.bot.register_next_step_handler(call.message, omb_find_map.find_by_date)

    elif call.data == "first_map":
        omb_types.map_pointer[call.message.chat.id][0] = 1
        omb_find_map.switch_map(call.message.chat.id, call.message.message_id)
    elif call.data == "prev_map":
        omb_types.map_pointer[call.message.chat.id][0] -= 1
        omb_find_map.switch_map(call.message.chat.id, call.message.message_id)
    elif call.data == "next_map":
        omb_types.map_pointer[call.message.chat.id][0] += 1
        omb_find_map.switch_map(call.message.chat.id, call.message.message_id)
    elif call.data == "last_map":
        omb_types.map_pointer[call.message.chat.id][0] = omb_types.map_pointer[call.message.chat.id][1]
        omb_find_map.switch_map(call.message.chat.id, call.message.message_id)
    elif call.data == "show_addfiles":
        omap = omb_types.user_maps[call.message.chat.id][omb_types.map_pointer[call.message.chat.id][0]-1]
        omap_id = omap[0]
        addfile_cnt = omap[10]
        omb_types.map_addfiles[omap_id] = omb_postgre.get_all_addfiles(omap_id)
        omb_types.bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=omb_types.map_switch_keyboard(
                omb_types.map_pointer[call.message.chat.id],
                addfile_cnt,
                show_addfiles=True,
                omap_id=omap_id))
    elif call.data == "hide_addfiles":
        omap = omb_types.user_maps[call.message.chat.id][omb_types.map_pointer[call.message.chat.id][0]-1]
        addfile_cnt = omap[10]
        omb_types.bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=omb_types.map_switch_keyboard(
                omb_types.map_pointer[call.message.chat.id],
                addfile_cnt,
                show_addfiles=False))
    elif call.data[:13] == "show_addfile_":
        addfile_id = int(call.data[13:])
        omb_find_map.show_addfile(call.message.chat.id, call.message.message_id, addfile_id)
    elif call.data == "map_switch_from_addfile":
        omb_find_map.switch_map(call.message.chat.id, call.message.message_id, show_addfiles=True)
    elif call.data == "admin_info":
        omb_types.bot.send_message(
            call.message.chat.id,
            '\n'.join([str(row[0]) + ' - ' + row[1] + ' - ' + row[2] + ' (' + str(row[3]) + ' maps)'
                       for row in omb_postgre.get_all_users()]))
    elif call.data == "show_geoloc":
        omb_find_map.show_geoloc(call.message.chat.id, call.message.message_id)
    elif call.data == "map_switch_from_geoloc":
        user_id = call.message.chat.id
        omb_find_map.switch_map_init(user_id)
    elif call.data == "delete_map":
        user_id = call.message.chat.id
        index = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0]-1][8]
        if index == "-":
            omb_types.bot.send_message(call.message.chat.id, 'Точно удаляем?',
                                       reply_markup=omb_types.map_delete_completely_confirm())
        else:
            omb_types.bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                                    reply_markup=omb_types.map_delete_mode())
    elif call.data == "delete_paper_map":
        omb_types.bot.send_message(call.message.chat.id, 'Точно удаляем?',
                                   reply_markup=omb_types.map_delete_paper_confirm())
    elif call.data == "delete_paper_map_yes":
        user_id = call.message.chat.id
        omap_id = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0] - 1][0]

        omb_postgre.delete_paper_map(user_id, omap_id)
        omb_types.bot.send_message(call.message.chat.id, 'Информация о бумажной карте удалена. Можно её выкинуть.')

        omb_types.bot.send_message(call.message.chat.id, 'Возвращаемся в главное меню',
                                   reply_markup=omb_types.welcome_keyboard(call.message.chat.id == 366436625))
    elif call.data == "delete_paper_map_no":
        user_id = call.message.chat.id
        omb_find_map.switch_map_init(user_id)
    elif call.data == "delete_completely":
        omb_types.bot.send_message(call.message.chat.id, 'Точно удаляем?',
                                   reply_markup=omb_types.map_delete_completely_confirm())
    elif call.data == "delete_completely_yes":
        user_id = call.message.chat.id
        omap_id = omb_types.user_maps[user_id][omb_types.map_pointer[user_id][0] - 1][0]

        omb_postgre.delete_completely(user_id, omap_id)
        omb_types.bot.send_message(call.message.chat.id, 'Карта удалена.')

        omb_types.bot.send_message(call.message.chat.id, 'Возвращаемся в главное меню',
                                   reply_markup=omb_types.welcome_keyboard(call.message.chat.id == 366436625))
    elif call.data == "delete_completely_no":
        user_id = call.message.chat.id
        omb_find_map.switch_map_init(user_id)
    elif call.data == "edit_map_file":
        # omb_types.bot.send_message(call.message.chat.id, "Укажи хэштэги")
        # omb_types.bot.register_next_step_handler(call.message, omb_edit_map.edit_tags)

        omb_types.bot.send_message(call.message.chat.id, '*Приложи карту.*', parse_mode='Markdown')
        omb_types.bot.register_next_step_handler(call.message, omb_edit_map.edit_map_file)
    elif call.data == "edit_event_date":
        omb_types.bot.send_message(call.message.chat.id,
                                   "Укажи дату в формате *DD.MM.YYYY*",
                                   parse_mode='Markdown')
        omb_types.bot.register_next_step_handler(call.message, omb_edit_map.edit_event_date)
    elif call.data == "edit_tags":
        omb_types.bot.send_message(call.message.chat.id, "Укажи хэштэги")
        omb_types.bot.register_next_step_handler(call.message, omb_edit_map.edit_tags)
    elif call.data == "edit_geoloc":
        omb_types.bot.send_message(call.message.chat.id, "Приложи геолокацию")
        omb_types.bot.register_next_step_handler(call.message, omb_edit_map.edit_geoloc)
    elif call.data == "edit_first_letter":
        omb_types.bot.send_message(call.message.chat.id, "Укажи индекс")
        omb_types.bot.register_next_step_handler(call.message, omb_edit_map.edit_first_letter)


@omb_types.bot.message_handler(commands=["start"])
def start(m):
    omb_start.start(m, admin_mode=(m.chat.id == 366436625))


@omb_types.bot.message_handler(commands=["description"])
def description(message):
    omb_start.description(message)


# Получение любых сообщений от юзера
@omb_types.bot.message_handler(content_types=["text"])
def handle_text(message):
    start(message)


omb_types.bot.infinity_polling()
