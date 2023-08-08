import mysql.connector
import configparser
import sys
from mysql.connector import Error

config = configparser.ConfigParser()
config.read('/opt/env/live/app/config.ini')
print(config.sections())
print(config['mysql']['user'])
try:
    connection = mysql.connector.connect(host=config['mysql']['host'],
                                         database=config['mysql']['database'],
                                         user=config['mysql']['user'],
                                         password=config['mysql']['password'])
    if connection.is_connected():
        db_info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_info)
        cursor = connection.cursor()
        cursor.execute("ALTER TABLE osticket_db.ost_ticket ADD lastreported DATETIME NULL;")
        connection.commit()
        print("Added column lastreported to table osticket_db for loging tickets reported to slack.")
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
