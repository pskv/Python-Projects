import psycopg2
from datetime import datetime, timezone
import orient_maps_bot_types as omb_types


with open('Orient_maps_bot/postgre_params.txt') as f:
    postgre_params_raw = f.read().strip()
postgre_params = dict()
for param in postgre_params_raw.split('\n'):
    postgre_params[param.split(':')[0]] = param.split(':')[1]


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
        omb_types.bot.send_message(366436625, "New user!\nuser_id: "+str(user_id)+"\nusername: "+username)
        print('123123')
        return user_id, 'ALLOWED'


def save_map_to_db(omap):
    conn = psycopg2.connect(dbname=postgre_params['dbname'], user=postgre_params['user'],
                            password=postgre_params['password'], host=postgre_params['host'])
    with conn.cursor() as cursor:
        insert = 'INSERT INTO ' + postgre_params['maps_table'] + \
                 ' (name,omap_type,longitude,latitude,event_date,' \
                 'tags,owner,omap_first_letter,telegram_file_id,' \
                 'upload_tmst) ' \
                 'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, current_timestamp) ' \
                 'RETURNING omap_id'
        cursor.execute(insert, (omap.name, omap.telegram_file_type,
                                omap.location['longitude'], omap.location['latitude'],
                                omap.event_date, omap.tags, omap.owner, omap.index,
                                omap.telegram_file_id))
        conn.commit()
        omap.id = cursor.fetchone()[0]
        select = 'select count(1) ' \
                 '  from ' + postgre_params['maps_table'] + ' t ' \
                                                            ' where owner = %s ' \
                                                            '   and omap_first_letter = %s'
        cursor.execute(select, (omap.owner, omap.index))
        cnt = cursor.fetchone()
        cursor.close()
    conn.close()
    log_db('save_map_to_db', str(omap.owner), 'omap_id: '+str(omap.id))
    return cnt


def check_maps_exist(user_id):
    conn = psycopg2.connect(dbname=postgre_params['dbname'],
                            user=postgre_params['user'],
                            password=postgre_params['password'],
                            host=postgre_params['host'])
    with conn.cursor() as cursor:
        cursor.execute("SELECT omap_id"
                       "  FROM " + postgre_params['maps_table'] + " m"
                       " WHERE owner = %s",
                       (user_id,))
        records = cursor.fetchone()
        cursor.close()
    conn.close()
    return len(records)>0


def get_all_maps(user_id):
    conn = psycopg2.connect(dbname=postgre_params['dbname'],
                            user=postgre_params['user'],
                            password=postgre_params['password'],
                            host=postgre_params['host'])
    with conn.cursor() as cursor:
        cursor.execute("SELECT omap_id, name, omap_type, longitude, latitude"
                       "     , event_date, tags, telegram_file_id"
                       "     , COALESCE(omap_first_letter,'-') as omap_first_letter"
                       "     , row_number() over(partition by COALESCE(omap_first_letter,'-')"
                       "            order by omap_seq nulls last,omap_id) as omap_letter_seq"
                       "     , (select count(1) "
                       "          from " + postgre_params['map_files_table'] + " mf"
                       "         where mf.omap_id = m.omap_id) as addfile_cnt"
                       "  FROM " + postgre_params['maps_table'] + " m"
                       " WHERE owner = %s "
                       " ORDER BY omap_id",
                       (user_id,))
        records = cursor.fetchall()
        cursor.close()
    conn.close()
    return records


def get_maps_by_first_letter(user_id, letter):
    conn = psycopg2.connect(dbname=postgre_params['dbname'],
                            user=postgre_params['user'],
                            password=postgre_params['password'],
                            host=postgre_params['host'])
    with conn.cursor() as cursor:
        cursor.execute("SELECT omap_id, name, omap_type, longitude, latitude"
                       "     , event_date, tags, telegram_file_id"
                       "     , COALESCE(omap_first_letter,'-') as omap_first_letter"
                       "     , row_number() over(partition by COALESCE(omap_first_letter,'-')"
                       "            order by omap_seq nulls last,omap_id) as omap_letter_seq"
                       "     , (select count(1) "
                       "          from " + postgre_params['map_files_table'] + " mf"
                       "         where mf.omap_id = m.omap_id) as addfile_cnt"
                       "  FROM " + postgre_params['maps_table'] + " m"
                       " WHERE owner = %s"
                       "   AND COALESCE(omap_first_letter,'-') = %s"
                       " ORDER BY omap_letter_seq",
                       (user_id, letter))
        records = cursor.fetchall()
        cursor.close()
    conn.close()
    return records


def get_stat_first_letter(user_id):
    conn = psycopg2.connect(dbname=postgre_params['dbname'],
                            user=postgre_params['user'],
                            password=postgre_params['password'],
                            host=postgre_params['host'])
    with conn.cursor() as cursor:
        cursor.execute("SELECT COALESCE(omap_first_letter,'-') as omap_first_letter"
                       "     , count(1) as cnt"
                       "  FROM " + postgre_params["maps_table"] +
                       " WHERE owner = %s"
                       " GROUP BY COALESCE(omap_first_letter,'-')"
                       " ORDER BY COALESCE(omap_first_letter,'-')",
                       (user_id, ))
        records = cursor.fetchall()
        cursor.close()
    conn.close()
    return records


def get_all_addfiles(omap_id):
    conn = psycopg2.connect(dbname=postgre_params['dbname'],
                            user=postgre_params['user'],
                            password=postgre_params['password'],
                            host=postgre_params['host'])
    with conn.cursor() as cursor:
        cursor.execute("SELECT file_id,omap_id,file_type,telegram_file_id,telegram_file_type"
                       "  FROM " + postgre_params['map_files_table'] + " m"
                       " WHERE omap_id = %s"
                       " ORDER BY file_id",
                       (omap_id,))
        records = cursor.fetchall()
        cursor.close()
    conn.close()
    return records


def save_file_to_db(addfile, user_id):
    conn = psycopg2.connect(dbname=postgre_params['dbname'], user=postgre_params['user'],
                            password=postgre_params['password'], host=postgre_params['host'])
    with conn.cursor() as cursor:
        insert = 'INSERT INTO ' + postgre_params['map_files_table'] + \
                 ' (omap_id,file_type,telegram_file_id,upload_tmst,telegram_file_type) ' \
                 'VALUES (%s, %s, %s, current_timestamp, %s) ' \
                 'RETURNING file_id'
        cursor.execute(insert, (addfile.omap_id,
                                addfile.file_type,
                                addfile.telegram_file_id,
                                addfile.telegram_file_type))
        conn.commit()
        addfile.file_id = cursor.fetchone()[0]
        cursor.close()
    conn.close()
    log_db('save_file_to_db', str(user_id), 'omap_id: '+str(addfile.omap_id)+', file_type: '+addfile.file_type)
    return addfile.file_id


def get_all_users():
    conn = psycopg2.connect(dbname=postgre_params['dbname'],
                            user=postgre_params['user'],
                            password=postgre_params['password'],
                            host=postgre_params['host'])
    with conn.cursor() as cursor:
        cursor.execute('SELECT user_id,username,access_mode, '
                       '(select count(1) from ' + postgre_params["maps_table"] +
                       ' m where m.owner = u.user_id) as maps_cnt'
                       ' FROM ' + postgre_params['users_table'] + ' u')
        records = cursor.fetchall()
        cursor.close()
    return records


def get_maps_by_tags(user_id, tag):
    conn = psycopg2.connect(dbname=postgre_params['dbname'],
                            user=postgre_params['user'],
                            password=postgre_params['password'],
                            host=postgre_params['host'])
    with conn.cursor() as cursor:
        cursor.execute("SELECT omap_id,name, omap_type, longitude, latitude"
                       "     , event_date, tags, telegram_file_id"
                       "     , coalesce(omap_first_letter,'-') as omap_first_letter"
                       "     , row_number() over(partition by coalesce(omap_first_letter,'-') "
                       "            order by omap_seq nulls last,omap_id) as omap_letter_seq"
                       "     , (select count(1) "
                       "          from " + postgre_params['map_files_table'] + " mf "
                       "          where mf.omap_id = m.omap_id) as addfile_cnt"
                       "  FROM " + postgre_params['maps_table'] + " m ,"
                       "       unnest(string_to_array(tags, ' ')) as tag"
                       " WHERE owner = %s"
                       "   AND lower(tag) = %s"
                       " ORDER BY event_date",
                       (user_id, tag))
        records = cursor.fetchall()
        cursor.close()
    conn.close()
    return records


def get_stat_tags(user_id):
    conn = psycopg2.connect(dbname=postgre_params['dbname'],
                            user=postgre_params['user'],
                            password=postgre_params['password'],
                            host=postgre_params['host'])
    with conn.cursor() as cursor:
        cursor.execute("select lower(unnest(string_to_array(tags, ' '))) as tag,"
                       "       count(1) as cnt"
                       "  from " + postgre_params["maps_table"] +
                       " where owner = %s "
                       " group by lower(unnest(string_to_array(tags, ' ')))"
                       " order by cnt, tag",
                       (user_id, ))
        records = cursor.fetchall()
        cursor.close()
    conn.close()
    return records


def get_maps_by_geoloc(user_id, location_long, location_lat):
    conn = psycopg2.connect(dbname=postgre_params['dbname'],
                            user=postgre_params['user'],
                            password=postgre_params['password'],
                            host=postgre_params['host'])
    with conn.cursor() as cursor:
        cursor.execute("SELECT omap_id, name, omap_type, longitude, latitude, event_date"
                       "     , tags, telegram_file_id, omap_first_letter, omap_letter_seq, addfile_cnt"
                       "     , round(acos(sin(lat1) * sin(lat2) "
                       "       + cos(lat1)*cos(lat2)*cos(lon2-lon1)) * 63710)/10 as dist"
                       "  FROM ("
                       "        select omap_id, name, omap_type, longitude, latitude, event_date"
                       "             , tags, telegram_file_id, coalesce(omap_first_letter,'-') as omap_first_letter"
                       "             , row_number() over (partition by coalesce(omap_first_letter,'-')"
                       "                    order by omap_seq nulls last,omap_id) as omap_letter_seq"
                       "             , (select count(1) "
                       "                  from " + postgre_params['map_files_table'] + " mf "
                       "                 where mf.omap_id = m.omap_id) as addfile_cnt"
                       "             , latitude * pi() / 180 as lat1"
                       "             , %s * pi() / 180 as lat2"
                       "             , longitude * pi() / 180 as lon1"
                       "             , %s * pi() / 180 as lon2"
                       "          from " + postgre_params['maps_table'] + " m"
                       "         where owner = %s ) a"
                       " ORDER BY dist",
                       (location_lat, location_long, user_id))
        records = cursor.fetchall()
        cursor.close()
    conn.close()
    return records


def get_maps_by_date(user_id, event_date):
    conn = psycopg2.connect(dbname=postgre_params['dbname'],
                            user=postgre_params['user'],
                            password=postgre_params['password'],
                            host=postgre_params['host'])
    with conn.cursor() as cursor:
        cursor.execute("SELECT omap_id, name, omap_type, longitude, latitude, event_date"
                       "     , tags, telegram_file_id, coalesce(omap_first_letter,'-') as omap_first_letter"
                       "     , row_number() over (partition by coalesce(omap_first_letter,'-') "
                       "            order by omap_seq nulls last,omap_id) as omap_letter_seq"
                       "     , (select count(1) "
                       "          from " + postgre_params['map_files_table'] + " mf"
                       "         where mf.omap_id = m.omap_id) as addfile_cnt"
                       "  FROM " + postgre_params['maps_table'] + " m"
                       " WHERE owner = %s"
                       " ORDER BY event_date",
                       (user_id,))
        records = cursor.fetchall()
        cursor.execute("select rn from "
                       " ("
                       "  select row_number() over (order by event_date) rn ,"
                       "  abs(%s - t.event_date) as diff_days,"
                       "  min(abs(%s - t.event_date)) over (partition by 1) as min_diff_days "
                       "  from orient_maps_bot.maps t "
                       " where owner = %s"
                       " ) t "
                       "where diff_days = min_diff_days",
                       (event_date, event_date, user_id,))
        pointer = cursor.fetchone()[0]
        cursor.close()
    conn.close()
    return records, pointer


def delete_paper_map(user_id, omap_id):
    conn = psycopg2.connect(dbname=postgre_params['dbname'],
                            user=postgre_params['user'],
                            password=postgre_params['password'],
                            host=postgre_params['host'])
    with conn.cursor() as cursor:
        cursor.execute("update " + postgre_params["maps_table"] +
                       "   set omap_first_letter = '-'" 
                       " where omap_id = %s ",
                       (omap_id, ))
        conn.commit()
        cursor.close()
    conn.close()
    log_db('delete_paper_map', user_id, 'omap_id: '+str(omap_id))
    return 0


def delete_completely(user_id, omap_id):
    conn = psycopg2.connect(dbname=postgre_params['dbname'],
                            user=postgre_params['user'],
                            password=postgre_params['password'],
                            host=postgre_params['host'])
    with conn.cursor() as cursor:
        cursor.execute("delete "
                       "  from " + postgre_params["map_files_table"] +
                       " where omap_id = %s ",
                       (omap_id,))
        cursor.execute("delete "
                       "  from " + postgre_params["maps_table"] +
                       " where omap_id = %s ",
                       (omap_id,))
        conn.commit()
        cursor.close()
    conn.close()
    log_db('delete_completely', user_id, 'omap_id: '+str(omap_id))
    return 0


def edit_event_date(user_id, omap_id, event_date):
    conn = psycopg2.connect(dbname=postgre_params['dbname'],
                            user=postgre_params['user'],
                            password=postgre_params['password'],
                            host=postgre_params['host'])
    with conn.cursor() as cursor:
        cursor.execute("update " + postgre_params["maps_table"] +
                       "   set event_date = %s" 
                       " where omap_id = %s ",
                       (event_date, omap_id))
        conn.commit()
        cursor.close()
    conn.close()
    log_db('edit_event_date', user_id, 'omap_id: '+str(omap_id)+', event_date:'+str(event_date))
    return 0


def edit_tags(user_id, omap_id, tags):
    conn = psycopg2.connect(dbname=postgre_params['dbname'],
                            user=postgre_params['user'],
                            password=postgre_params['password'],
                            host=postgre_params['host'])
    with conn.cursor() as cursor:
        cursor.execute("update " + postgre_params["maps_table"] +
                       "   set tags = %s" 
                       " where omap_id = %s ",
                       (tags, omap_id))
        conn.commit()
        cursor.close()
    conn.close()
    log_db('edit_tags', user_id, 'omap_id: '+str(omap_id)+', tags:'+tags)
    return 0


def edit_map_file(user_id, omap_id, name, telegram_file_type, telegram_file_id):
    conn = psycopg2.connect(dbname=postgre_params['dbname'],
                            user=postgre_params['user'],
                            password=postgre_params['password'],
                            host=postgre_params['host'])
    with conn.cursor() as cursor:
        cursor.execute("update " + postgre_params["maps_table"] +
                       "   set name = %s"
                       "     , omap_type = %s"
                       "     , telegram_file_id = %s" 
                       " where omap_id = %s",
                       (name, telegram_file_type, telegram_file_id, omap_id))
        conn.commit()
        cursor.close()
    conn.close()
    log_db('edit_map_file', user_id, 'omap_id: '+str(omap_id)+', name:'+name)
    return 0


def edit_geoloc(user_id, omap_id, location_lat, location_long):
    conn = psycopg2.connect(dbname=postgre_params['dbname'],
                            user=postgre_params['user'],
                            password=postgre_params['password'],
                            host=postgre_params['host'])
    with conn.cursor() as cursor:
        cursor.execute("update " + postgre_params["maps_table"] +
                       "   set latitude = %s"
                       "     , longitude = %s" 
                       " where omap_id = %s",
                       (location_lat, location_long, omap_id))
        conn.commit()
        cursor.close()
    conn.close()
    log_db('edit_geoloc', user_id, 'omap_id: '+str(omap_id)+', location_lat:'+str(location_lat)+', location_long:'+str(location_long))
    return 0


def edit_first_letter(user_id, omap_id, index):
    conn = psycopg2.connect(dbname=postgre_params['dbname'],
                            user=postgre_params['user'],
                            password=postgre_params['password'],
                            host=postgre_params['host'])
    with conn.cursor() as cursor:
        get_nextval = "SELECT nextval('" + postgre_params['maps_table'] + "_omap_id_seq')"
        cursor.execute(get_nextval)
        new_omap_id = cursor.fetchone()[0]

        update = 'UPDATE ' + postgre_params['maps_table'] + \
                 '   SET omap_id = %s' \
                 '     , omap_first_letter = %s' \
                 ' WHERE omap_id = %s'
        cursor.execute(update, (new_omap_id, index, omap_id))
        conn.commit()

        select = 'select count(1) ' \
                 '  from ' + postgre_params['maps_table'] + ' t ' \
                 ' where owner = %s ' \
                 '   and omap_first_letter = %s'
        cursor.execute(select, (user_id, index))
        cnt = cursor.fetchone()
        cursor.close()
    conn.close()
    log_db('edit_first_letter', user_id, 'omap_id: '+str(omap_id)+', index:'+index)
    return cnt
