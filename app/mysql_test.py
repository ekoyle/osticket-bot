import mysql.connector
import configparser
import sys
from mysql.connector import Error

config = configparser.ConfigParser()
config.read('config.ini')
print(config.sections())
try:
    connection = mysql.connector.connect(host=config['mysql']['host'],
                                         database=config['mysql']['database'],
                                         user=config['mysql']['user'],
                                         password=config['mysql']['password'])
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
