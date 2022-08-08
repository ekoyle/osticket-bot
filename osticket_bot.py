# SELECT * FROM osticket_db.ost_ticket join osticket_db.ost_ticket__cdata on osticket_db.ost_ticket__cdata.ticket_id  = osticket_db.ost_ticket.ticket_id;

import json
import mysql.connector
from mysql.connector import Error
import requests
import sys
import getopt
import datetime;
import configparser
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError



def report(config, channel, message):
    print("Channel: %s " % channel)
    print("Message: %s " % message)
    client = WebClient(config['slack']['oauth_token'])
    try:
        response = client.chat_postMessage(channel='#bottest', text=message)
        print(response)
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")

def pullTickets(config):
    tickets = None

    try:
        connection = mysql.connector.connect(host=config['mysql']['host'],
                                         database=config['mysql']['database'],
                                         user=config['mysql']['user'],
                                         password=config['mysql']['password'])
    
        sql_select_Query = """ SELECT * FROM osticket_db.ost_ticket join osticket_db.ost_ticket__cdata
                           on osticket_db.ost_ticket__cdata.ticket_id  = osticket_db.ost_ticket.ticket_id where lastreported is null
                           """ 
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        # get all records
        records = cursor.fetchall()
        tickets =  records 
    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print("MySQL connection is closed")

    return tickets


def main():
    config = configparser.ConfigParser()
    config.read('botconfig.ini')
    print(config.sections())
    verbose = 0 
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "v")
    except:
        print("Error")

    for opt, arg in opts:

        if opt in ['-v']:
            verbose = 1

    tickets = pullTickets(config)
    print(tickets)
    for ticket in tickets:
        print(config['slack']['channel'])
        message = "New Ticket: %s, url: https://osticket.bhnoc.org/upload/scp/tickets.php?id=%s" % (ticket[29],ticket[0])
        report(config,config['slack']['channel'],message)



if __name__ == "__main__":
    main()
