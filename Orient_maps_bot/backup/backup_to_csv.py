from datetime import datetime
import psycopg2
from zipfile import ZipFile
import os


with open('../Orient_maps_bot/postgre_params_umovie.txt') as f:
    postgre_params_raw = f.read().strip()
postgre_params = dict()
for param in postgre_params_raw.split('\n'):
    postgre_params[param.split(':')[0]] = param.split(':')[1]

zipObj = ZipFile('backup_' + datetime.now().strftime("%Y%m%d_%H%M%S") + '.zip', 'w')

conn = psycopg2.connect(dbname=postgre_params['dbname'], user=postgre_params['user'],
                        password=postgre_params['password'], host=postgre_params['host'])
with conn.cursor() as cursor:
    sql = 'SELECT * FROM ' + postgre_params['maps_table']
    SQL_for_file_output = ("COPY ({0}) TO STDOUT WITH DELIMITER ';' CSV HEADER QUOTE '"+'"'+"'").format(sql)
    with open('maps.csv', 'w') as csvfile:
        cursor.copy_expert(SQL_for_file_output, csvfile)
    zipObj.write(csvfile.name)
    os.remove(csvfile.name)

    sql = 'SELECT * FROM ' + postgre_params['map_files_table']
    SQL_for_file_output = ("COPY ({0}) TO STDOUT WITH DELIMITER ';' CSV HEADER QUOTE '"+'"'+"'").format(sql)
    with open('map_files.csv', 'w') as csvfile:
        cursor.copy_expert(SQL_for_file_output, csvfile)
    zipObj.write(csvfile.name)
    os.remove(csvfile.name)

    sql = 'SELECT * FROM ' + postgre_params['users_table']
    SQL_for_file_output = ("COPY ({0}) TO STDOUT WITH DELIMITER ';' CSV HEADER QUOTE '"+'"'+"'").format(sql)
    with open('users.csv', 'w') as csvfile:
        cursor.copy_expert(SQL_for_file_output, csvfile)
    zipObj.write(csvfile.name)
    os.remove(csvfile.name)

    sql = 'SELECT * FROM ' + postgre_params['log_table']
    SQL_for_file_output = ("COPY ({0}) TO STDOUT WITH DELIMITER ';' CSV HEADER QUOTE '"+'"'+"'").format(sql)
    with open('log.csv', 'w') as csvfile:
        cursor.copy_expert(SQL_for_file_output, csvfile)
    zipObj.write(csvfile.name)
    os.remove(csvfile.name)
conn.close()
zipObj.close()

input("Backup successfully completed!\nPress any key to close this window...")
