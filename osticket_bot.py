# SELECT * FROM osticket_db.ost_ticket join osticket_db.ost_ticket__cdata on osticket_db.ost_ticket__cdata.ticket_id  = osticket_db.ost_ticket.ticket_id;

import json
import requests
import sys
import getopt
import datetime;
import configparser


def main():
    config = configparser.ConfigParser()
    config.read('botconfig.ini')
    print(config.sections())

    target_to_filter = None
    verbose = 0

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "v")
    except:
        print("Error")

    for opt, arg in opts:

        if opt in ['-v']:
            verbose = 1

            import mysql.connector

    try:
        connection = mysql.connector.connect(host=config['mysql']['host'],
                                         database=config['mysql']['database'],
                                         user=config['mysql']['user'],
                                         password=config['mysql']['password'])
    
        sql_select_Query = "select * from Laptop"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        # get all records
        records = cursor.fetchall()
        print("Total number of rows in table: ", cursor.rowcount)
    
        print("\nPrinting each row")
        for row in records:
            print("Id = ", row[0], )
            print("Name = ", row[1])
            print("Price  = ", row[2])
            print("Purchase date  = ", row[3], "\n")
    
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print("MySQL connection is closed")
